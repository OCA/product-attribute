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
    def _default_name(self):
        seq_policy = self._get_sequence_policy()
        if seq_policy != "product":
            return self.env["ir.sequence"].next_by_code("stock.lot.serial")
        return ""

    @api.onchange("product_id")
    def onchange_product_id(self):
        seq_policy = self._get_sequence_policy()
        if (
            seq_policy == "product"
            and self.product_id
            and self.product_id.product_tmpl_id.lot_sequence_id
        ):
            self.name = self.product_id.product_tmpl_id.lot_sequence_id._next()

    @api.model_create_multi
    def create(self, vals_list):
        seq_policy = self._get_sequence_policy()
        if seq_policy in ["product", "global"]:
            for lot_vals in vals_list:
                if "name" not in lot_vals:
                    if seq_policy == "product":
                        product = self.env["product.product"].browse(
                            lot_vals["product_id"]
                        )
                        if product and product.product_tmpl_id.lot_sequence_id:
                            lot_vals[
                                "name"
                            ] = product.product_tmpl_id.lot_sequence_id._next()
                    else:
                        lot_vals["name"] = self.env["ir.sequence"].next_by_code(
                            "stock.lot.serial"
                        )
        return super(StockLot, self).create(vals_list)

    @api.model
    def _get_next_serial(self, company, product):
        if "force_next_serial" in self.env.context:
            return self.env.context.get("force_next_serial")
        seq_policy = self._get_sequence_policy()
        if seq_policy == "product":
            seq = product.product_tmpl_id.lot_sequence_id
            if seq:
                return seq._next()
        elif seq_policy == "global":
            return self.env["ir.sequence"].next_by_code("stock.lot.serial")
        return super()._get_next_serial(company, product)
