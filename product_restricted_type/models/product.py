# Copyright 2018 ForgeFlow S.L.
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


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.onchange("categ_id")
    def _onchange_categ_id(self):
        if self.categ_id and self.categ_id.restricted_product_type:
            self.type = self.categ_id.restricted_product_type

    @api.onchange("type")
    def _onchange_type(self):
        if self.type:
            return {
                "domain": {
                    "categ_id": [("restricted_product_type", "in", [self.type, False])]
                }
            }
        else:
            return {"domain": {"categ_id": []}}
