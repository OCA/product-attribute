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
        return super().create(vals_list)

    @api.model
    def _get_next_serial(self, company, product):
        if "force_next_serial" in self.env.context:
            return self.env.context.get("force_next_serial")
        sequence = self._get_name_sequence(product)
        if sequence:
            return sequence._next()
        return super()._get_next_serial(company, product)
