# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[("supplierinfo", "Prices based on supplier info")],
        ondelete={"supplierinfo": "set default"},
    )
    no_supplierinfo_min_quantity = fields.Boolean(
        string="Ignore Supplier Info Min. Quantity",
    )
    filter_supplier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Supplier filter",
        help="Only match prices from the selected supplier",
    )

    def _compute_price(self, product, quantity, uom, date, currency=None):
        result = super()._compute_price(product, quantity, uom, date, currency)
        context = self.env.context
        if self.compute_price == "formula" and self.base == "supplierinfo":
            result = product.sudo()._get_supplierinfo_pricelist_price(
                self,
                date=date or context.get("date", fields.Date.today()),
                quantity=quantity,
            )
        return result
