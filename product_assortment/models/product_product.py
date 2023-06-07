# Copyright 2023 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    assortment_ids = fields.Many2many("ir.filters", readonly=True)

    # The following two method can be inherited
    # in order to add special action after adding or removing
    # a product from an assortment
    def _add_product_in_assortment(self, assortment):
        self.write({"assortment_ids": [fields.Command.link(assortment.id)]})

    def _remove_product_from_assortment(self, assortment):
        self.write({"assortment_ids": [fields.Command.unlink(assortment.id)]})
