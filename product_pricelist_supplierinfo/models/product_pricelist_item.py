# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2024 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


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

    def _is_applicable_for(self, product, qty_in_product_uom):
        res = True
        if self.base == "supplierinfo" and self.applied_on == "2_product_category":
            if (
                product.categ_id != self.categ_id
                and not product.categ_id.parent_path.startswith(
                    self.categ_id.parent_path
                )
            ) or self.filter_supplier_id.id not in product.seller_ids.mapped(
                "partner_id"
            ).ids:
                res = False
        elif self.base == "pricelist":
            if self.base_pricelist_id:
                for item in self.base_pricelist_id.item_ids:
                    if item._is_applicable_for(product, qty_in_product_uom):
                        res = True
                        break

                    res = False
        else:
            res = super()._is_applicable_for(product, qty_in_product_uom)
        return res
