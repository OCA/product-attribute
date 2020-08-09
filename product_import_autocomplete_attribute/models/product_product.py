# © 2020 Akretion France
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    def load(self, fields, data):
        result = super().load(fields, data)
        if result["ids"]:
            self.browse(result["ids"]).mapped(
                "product_tmpl_id"
            ).sync_attrs_from_variants()
        return result

    @api.model_create_multi
    def create(self, vals):
        if self.env.context.get("from_sync_attrs_from_variants"):
            for val in vals:
                val["active"] = False
        return super().create(vals)

    @api.multi
    def write(self, vals):
        if self.env.context.get("from_sync_attrs_from_variants") and vals.get(
            "active"
        ):
            vals["active"] = False
        return super().write(vals)
