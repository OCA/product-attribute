# Copyright 2020 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class StockLot(models.Model):
    _inherit = "stock.lot"

    name = fields.Char(default=lambda self: self._default_name())

    @api.model
    def _get_sequence_policy(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_lot_sequence.policy")
        )

    @api.model
    def _consume_on_create(self):
        """Whether a proposed name only takes its number once the lot exists"""
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_lot_sequence.consume_on_create")
            == "True"
        )

    @api.model
    def _get_duplicate_check_policy(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_lot_sequence.duplicate_check", "no")
        )

    @api.model
    def _get_name_sequence(self, product=None):
        """Return the correct sequence for the lot, empty when none applies"""
        seq_policy = self._get_sequence_policy()
        if seq_policy == "product":
            if product:
                return product.product_tmpl_id.lot_sequence_id
        elif seq_policy == "global":
            return self.env["ir.sequence"].search(
                [
                    ("code", "=", "stock.lot.serial"),
                    ("company_id", "in", [self.env.company.id, False]),
                ],
                order="company_id",
                limit=1,
            )
        return self.env["ir.sequence"]

    @api.model
    def _peek_next_name(self, product=None):
        """Get the next name without consuming it to avoid gaps"""
        sequence = self._get_name_sequence(product)
        if not sequence:
            return ""
        return sequence._lot_name_for(
            sequence._get_current_sequence().number_next_actual
        )

    @api.model
    def _propose_next_name(self, product=None):
        """Propose name for a lot that does not exist yet

        With ``consume_on_create`` the number is only read, so canceling doesn't leave
        a gap, the sequence is consumed only in ``create`` instead.
        Without ``consume_on_create`` the number is consumed here, which is was the
        original behaviour
        """
        if self._consume_on_create():
            return self._peek_next_name(product)
        sequence = self._get_name_sequence(product)
        return sequence._next() if sequence else ""

    @api.model
    def _default_name(self):
        return self._propose_next_name()

    @api.model
    def generate_lot_names(self, first_lot, count):
        # number the batch from the sequence, not from the name's digits: core
        # increments the last run of digits it finds, which merges with prefix
        # (ABC2026) and suffix (3M) digits into one number, "ABC20260000013M"
        sequence = self._get_name_sequence()
        match = sequence and sequence._lot_name_regex().match(first_lot or "")
        if not match:
            return super().generate_lot_names(first_lot, count)
        first = int(match.group(1))
        return [
            {"lot_name": sequence._lot_name_for(first + index)}
            for index in range(count)
        ]

    def _lots_by_sequence(self):
        """Group the lots by the sequence their names should follow"""
        seq_policy = self._get_sequence_policy()
        if seq_policy == "global":
            sequence = self._get_name_sequence()
            return {sequence: self} if sequence else {}
        if seq_policy == "product":
            grouped = self.grouped(lambda lot: lot.product_id.product_tmpl_id)
            return {
                template.lot_sequence_id: lots
                for template, lots in grouped.items()
                if template.lot_sequence_id
            }
        return {}

    def _resync_sequence(self):
        """Advance each sequence past the names carried by these lots"""
        for sequence, lots in self._lots_by_sequence().items():
            sequence._resync_from_lot_names(lots.mapped("name"))

    def _check_lot_name_available(self):
        """Refuse a sequence name that already exists"""
        policy = self._get_duplicate_check_policy()
        if policy == "no":
            return
        if policy == "admin" and self.env.user.has_group("base.group_system"):
            return
        matching_ids = set()
        for sequence, lots in self._lots_by_sequence().items():
            regex = sequence._lot_name_regex()
            matching_ids.update(lot.id for lot in lots if regex.match(lot.name or ""))
        candidates = self.browse(matching_ids)
        if not candidates:
            return
        # pair the lot name and company for the filtering to handle cases where lot
        # company_id is not filled
        taken = {(lot.name, lot.company_id.id) for lot in candidates}
        duplicates = (
            self.sudo()
            .search(
                [
                    ("id", "not in", candidates.ids),
                    ("name", "in", candidates.mapped("name")),
                ]
            )
            .filtered(lambda lot: (lot.name, lot.company_id.id) in taken)
        )
        if duplicates:
            raise UserError(
                self.env._(
                    "The serial numbers %(names)s are already used by another"
                    " product. Generate a new set and try again.",
                    names=duplicates.mapped("name"),
                )
            )

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self._get_sequence_policy() == "product" and self.product_id:
            name = self._propose_next_name(self.product_id)
            if name:
                self.name = name

    @api.model_create_multi
    def create(self, vals_list):
        seq_policy = self._get_sequence_policy()
        if seq_policy not in ("product", "global"):
            return super().create(vals_list)
        for lot_vals in vals_list:
            if lot_vals.get("name"):
                continue
            product = self.env["product.product"].browse(lot_vals.get("product_id"))
            sequence = self._get_name_sequence(product)
            if sequence:
                lot_vals["name"] = sequence._next()
        lots = super().create(vals_list)
        lots._check_lot_name_available()
        lots._resync_sequence()
        return lots

    @api.model
    def _get_next_serial(self, company, product):
        if "force_next_serial" in self.env.context:
            return self.env.context.get("force_next_serial")
        name = self._propose_next_name(product)
        if name:
            return name
        return super()._get_next_serial(company, product)
