# Copyright 2024 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class ProductOptionalLine(models.Model):
    _name = "product.optional.line"
    _description = "Optional Product"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        domain="[('id', '!=', optional_product_tmpl_id)]",
        string="Related Product",
        required=True,
    )
    company_id = fields.Many2one(related="product_tmpl_id.company_id")
    optional_product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        domain="[('company_id', 'in', [company_id, False]), ('id', '!=', product_tmpl_id)]",
        string="Product",
        required=True,
    )
    quantity = fields.Float(
        default=1.0,
    )

    @api.constrains("product_tmpl_id", "optional_product_tmpl_id")
    def _check_same_product_as_related(self):
        """
        Restrict setting product template this line is related to as optional.
        """
        for r in self:
            if (
                r.product_tmpl_id
                and r.optional_product_tmpl_id
                and r.product_tmpl_id == r.optional_product_tmpl_id
            ):
                raise models.ValidationError(
                    _("You can't add product this line is related to as optional.")
                )

    @api.constrains("product_tmpl_id", "optional_product_tmpl_id")
    def _check_unique_products_within_product(self):
        """
        Make sure that all of the optional products are unique.
        """
        for r in self:
            if self.search_count(
                [
                    ("optional_product_tmpl_id", "=", r.optional_product_tmpl_id.id),
                    ("product_tmpl_id", "=", r.product_tmpl_id.id),
                    ("id", "!=", r.id),
                ]
            ):
                raise models.ValidationError(
                    _("You can't add two same products as optional.")
                )
