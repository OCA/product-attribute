# Copyright 2020 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductPricelistPrint(models.TransientModel):
    _inherit = "product.pricelist.print"

    is_public_categ = fields.Boolean(string="Filter/Group by public categories")

    public_categ_ids = fields.Many2many(
        "product.public.category", string="Website Product Category"
    )

    def get_products_domain(self):
        domain = super().get_products_domain()
        if self.public_categ_ids:
            domain.append(("public_categ_ids", "in", self.public_categ_ids.ids))
        return domain

    def get_group_key(self, product):
        if self.is_public_categ:
            if product.public_categ_ids:
                return product.public_categ_ids[:1].name
            else:
                return ""
        return super().get_group_key(product)
