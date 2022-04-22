# Copyright 2021 Camptocamp SA
# @author: Julien Coux <julien.coux@camptocamp.com>
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductAllowedList(models.Model):
    _name = "product.allowed.list"
    _description = "Product list configuration"

    name = fields.Char(required=True)
    line_ids = fields.One2many(
        comodel_name="product.allowed.list.line",
        inverse_name="product_list_id",
        string="Lines",
        copy=True,
    )

    def config_for_product(self, prod):
        """Retrieve current configuration for given product."""
        return self.line_ids.find_for_product(prod, config=self)
