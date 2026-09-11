# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    net_weight = fields.Float(
        compute="_compute_net_weight",
        store=True,
        readonly=False,
        digits="Stock Weight",
        help="Weight of the packaging content without container nor packaging.",
    )

    @api.depends("product_id.uom_id", "uom_id.factor")
    def _compute_net_weight(self):
        for packaging in self:
            packaging.net_weight = packaging.product_id.net_weight * packaging.qty

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        # OVERRIDE to add the uom to the field label
        res = super().fields_get(allfields, attributes)
        if self.env.context.get("uom_inline_field_labels"):
            if "net_weight" in res and "string" in res["net_weight"]:
                ProductTemplate = self.env["product.template"]
                weight_uom_name = (
                    ProductTemplate._get_weight_uom_name_from_ir_config_parameter()
                )
                res["net_weight"]["string"] += f" ({weight_uom_name})"
        return res
