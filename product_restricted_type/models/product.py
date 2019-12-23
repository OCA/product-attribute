# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _inherit = "product.category"

    restricted_product_type = fields.Selection(
        string="Restricted Product Type",
        selection=lambda self: self.env["product.template"]._fields["type"].selection,
    )

    @api.constrains("restricted_product_type")
    def _check_restricted_product_type(self):
        """Check if any product in the category has different type"""
        for categ in self:
            if categ.restricted_product_type:
                products = self.env["product.template"].search(
                    [
                        ("categ_id", "=", categ.id),
                        ("type", "!=", categ.restricted_product_type),
                    ],
                    limit=1,
                )
                if products:
                    raise ValidationError(
                        _(
                            "A product (or multiple products) in the category "
                            "have different type than the selected restricted "
                            "product type"
                        )
                    )
