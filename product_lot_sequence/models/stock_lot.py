# Copyright 2020 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


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
    def _default_name(self):
        sequence = self._get_name_sequence()
        return sequence._next() if sequence else ""

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
            by_sequence = {}
            grouped = self.grouped(lambda lot: lot.product_id.product_tmpl_id)
            for template, lots in grouped.items():
                sequence = template.lot_sequence_id
                if not sequence:
                    continue
                # several templates may point at one sequence, so accumulate
                by_sequence[sequence] = by_sequence.get(sequence, self.browse()) | lots
            # callers lock these in order: sort so two batches holding the same
            # sequences cannot take them in opposite order and deadlock
            return dict(sorted(by_sequence.items(), key=lambda item: item[0].id))
        return {}

    def _resync_sequence(self):
        """Advance each sequence past the names carried by these lots"""
        for sequence, lots in self._lots_by_sequence().items():
            sequence._resync_from_lot_names(lots.mapped("name"))

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self._get_sequence_policy() == "product" and self.product_id:
            sequence = self._get_name_sequence(self.product_id)
            if sequence:
                self.name = sequence._next()

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
        lots._resync_sequence()
        return lots

    @api.model
    def _get_next_serial(self, company, product):
        if "force_next_serial" in self.env.context:
            return self.env.context.get("force_next_serial")
        sequence = self._get_name_sequence(product)
        if sequence:
            return sequence._next()
        return super()._get_next_serial(company, product)
