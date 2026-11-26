from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_template_variant_value_ids = fields.Many2many(
        domain=lambda self: self._get_domain_attribute_line_id(),
    )

    def _get_domain_attribute_line_id(self):
        domoain = [
            "|",
            ("attribute_line_id.value_count", ">", 1),
            ("attribute_line_id.attribute_id.single_variant_attribute", "=", True),
        ]
        return domoain
