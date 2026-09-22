# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
import re

from odoo import models
from odoo.exceptions import UserError

# Width of every ir.sequence date placeholder that _get_prefix_suffix interpolates
PLACEHOLDER_WIDTHS = {
    "year": 4,
    "month": 2,
    "day": 2,
    "y": 2,
    "doy": 3,
    "woy": 2,
    "weekday": 1,
    "h24": 2,
    "h12": 2,
    "min": 2,
    "sec": 2,
}

# matches one placeholder of an odoo prefix:
# In "P%(year)s" matching "%(year)s" and capturing "year"
PLACEHOLDER_RE = re.compile(r"%\((\w+)\)s")


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    def _lot_name_pattern(self, text):
        r"""Regex matching a prefix or suffix, including placeholders

        "ABC" -> "ABC"
        "P%(year)s" -> "P\d{4}"
        "%(range_year)s/%(month)s-" -> "\d{4}/\d{2}-"
        """
        parts = []
        position = 0  # end of the last placeholder / start of the next literal
        text = text or ""
        for match in PLACEHOLDER_RE.finditer(text):
            # prefix may hold regex metacharacters: "A.C" must not match "ABC"
            parts.append(re.escape(text[position : match.start()]))
            # year, range_year and current_year have all same width: 4
            key = match.group(1).removeprefix("range_").removeprefix("current_")
            if key not in PLACEHOLDER_WIDTHS:
                raise UserError(
                    self.env._(
                        "Sequence %(sequence)s uses the unsupported placeholder"
                        " %(placeholder)s.",
                        sequence=self.display_name,
                        placeholder=match.group(0),
                    )
                )
            # a fixed width stops digit matching correctly
            # %(year)s -> width 4 -> "20200001" -> "2020"
            parts.append(rf"\d{{{PLACEHOLDER_WIDTHS[key]}}}")
            position = match.end()
        # add the remaining literal after the placeholders
        parts.append(re.escape(text[position:]))
        return "".join(parts)

    def _lot_name_regex(self):
        """Match the names this sequence produces, capturing their number"""
        self.ensure_one()
        # prefix "ABC" -> "^ABC(\d+)$", so "ABC0000101" gives 101
        # prefix "P%(year)s" -> "^P\d{4}(\d+)$", so "P202600012" gives 12
        # prefix "SN" suffix "/X" -> "^SN(\d+)/X$", so "SN000150/Y" does not match.
        return re.compile(
            rf"^{self._lot_name_pattern(self.prefix)}(\d+){self._lot_name_pattern(self.suffix)}$"
        )

    def _lot_name_for(self, number):
        """Name this sequence gives to `number`, consuming nothing"""
        self.ensure_one()
        sequence = self
        if self.use_date_range:
            # get_next_char reads range_* placeholders from the context
            sequence = self.with_context(
                ir_sequence_date_range=self._get_current_sequence().date_from
            )
        return sequence.get_next_char(number)

    def _lock(self):
        """Serialise transactions that read this sequence"""
        self.ensure_one()
        self.env.cr.execute(
            "SELECT id FROM ir_sequence WHERE id = %s FOR NO KEY UPDATE", [self.id]
        )

    def _resync_from_lot_names(self, names):
        """Move the sequence past ``names`` so none of them is ever reissued.

        Only names this sequence could have produced are considered, and the
        counter is never moved backwards.
        """
        self.ensure_one()
        regex = self._lot_name_regex()
        numbers = [int(match.group(1)) for match in map(regex.match, names) if match]
        if not numbers:
            return
        self._lock()
        current = self._get_current_sequence()
        current.invalidate_recordset(["number_next_actual"])
        highest = max(numbers)
        if current.number_next_actual <= highest:
            current.sudo().number_next_actual = highest + 1
