# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    unit_price = fields.Float(related="product_id.list_price")
    sale_price = fields.Float(compute="_compute_sale_price", digits="Product Price")
    # Only used by the wizard to display the computed price in the treeview
    packaging_wizard_price = fields.Float(store=False, digits="Product Price")

    @api.depends("unit_price", "qty")
    def _compute_sale_price(self):
        for record in self:
            record.sale_price = record.unit_price * record.qty
