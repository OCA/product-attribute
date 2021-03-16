# © 2020 Akretion France
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    attribute_value_ids = fields.Many2many(
        "product.attribute.value",
        compute="_compute_attribute_value_ids",
        )

    def _compute_attribute_value_ids(self):
        for record in self:
            record.attribute_value_ids =\
                record.product_template_attribute_value_ids.product_attribute_value_id

    @api.model_create_multi
    def create(self, list_vals):
        super_list_vals = []
        records = self
        for vals in list_vals:
            if "attribute_value_ids" in vals:
                tmpl = self.env["product.template"].browse(vals["product_tmpl_id"])
                value_ids = vals.get("attribute_value_ids", [(6, 0, [])])[0][2]
                values = self.env["product.attribute.value"].browse(value_ids)
                tmpl.update_attribute(values)
                variant = tmpl._get_existing_variant(values)
                variant.write(vals)
                records |= variant
            else:
                super_list_vals.append(vals)
        return records + super().create(super_list_vals)
