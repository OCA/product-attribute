# Copyright 2018-2024 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    allowed_categ_ids = fields.Many2many(
        "product.category",
        compute="_compute_allowed_categ_ids",
        string="Allowed Categories",
    )

    @api.onchange("categ_id")
    def _onchange_categ_id(self):
        # When creating a new Product, assign first the type based on the
        # default category. After that, the assignation is restricted
        # with the `allowed_categ_ids`
        if self.categ_id and self.categ_id.restricted_product_type:
            self.detailed_type = self.categ_id.restricted_product_type

    @api.depends("type")
    def _compute_allowed_categ_ids(self):
        allowed_categ_ids_dict = dict()
        for product_type in self.mapped("type"):
            allowed_categ_ids_from_type = self.env["product.category"].search(
                [("restricted_product_type", "in", [product_type, False])]
            )
            allowed_categ_ids_dict.setdefault(product_type, allowed_categ_ids_from_type)
        for record in self:
            record.allowed_categ_ids = allowed_categ_ids_dict.get(record.type, False)

    @api.constrains("type")
    def _check_product_type(self):
        type_dict = dict(self._fields["type"]._description_selection(self.env))
        for product in self:
            if (
                product.categ_id.restricted_product_type
                and product.type != product.categ_id.restricted_product_type
            ):
                msg = _(
                    "The Product Type (%(product_type)s) must be equal to the "
                    "Restricted Product Type defined in the Product Category "
                    "(%(product_categ_restricted_type)s).",
                    product_type=type_dict.get(product.type),
                    product_categ_restricted_type=type_dict.get(
                        product.categ_id.restricted_product_type
                    ),
                )
                raise ValidationError(msg)
