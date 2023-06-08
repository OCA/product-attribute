# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"


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

    def get_supplier_id(self):
        self.ensure_one()
        supplier_id = self._context.get("supplier") or self.filter_supplier_id.id
        return self.env["res.partner"].browse(supplier_id)

    def _compute_price(self, price, price_uom, product, quantity=1.0, partner=False):
        if self.compute_price == "formula" and self.base == "supplierinfo":
            context = self.env.context
            price = product.sudo()._get_supplierinfo_pricelist_price(
                self,
                date=context.get("date", fields.Date.today()),
                quantity=quantity,
                partner=partner,
            )
        # Re-use existing method that will apply discount/rounding/surcharge/margin
        price = super()._compute_price(price, price_uom, product, quantity, partner)
        return price
