# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class UomUom(models.Model):
    _inherit = "uom.uom"

    # Only used by the wizard to display the computed price in the treeview
    packaging_wizard_price = fields.Float(store=False, digits="Product Price")


class ProductUom(models.Model):
    _inherit = "product.uom"

    sale_price = fields.Float(
        compute="_compute_sale_price",
        digits="Product Price",
        help=(
            "The sale price of the product packaging computed from "
            "the product list price and the packaging factor."
        ),
    )

    @api.depends("product_id.lst_price", "uom_id.factor")
    def _compute_sale_price(self):
        for record in self:
            record.sale_price = (
                record.product_id.lst_price * record.uom_id.factor
                if record.uom_id
                else 0.0
            )
