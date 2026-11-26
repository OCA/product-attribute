# Copyright 2026 Marcos Mendez <m@pop.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    base = fields.Selection(
        selection_add=[("fifo_oldest_cost", "FIFO Cost (oldest lot in stock)")],
        ondelete={"fifo_oldest_cost": "set default"},
    )

    def _get_price_label_base_str(self):
        if self.base == "fifo_oldest_cost":
            return self.env._("FIFO cost of the oldest lot")
        return super()._get_price_label_base_str()

    def _compute_base_price(self, product, quantity, uom, date, currency):
        if self.base != "fifo_oldest_cost":
            return super()._compute_base_price(product, quantity, uom, date, currency)
        company = self.pricelist_id.company_id or self.env.company
        layer = self._get_oldest_stock_layer(product, company)
        if layer:
            price = layer.unit_cost
            target_uom = uom or product.uom_id
            if target_uom != product.uom_id:
                price = product.uom_id._compute_price(price, target_uom)
        else:
            # Nothing left in stock: the product cost, as the core "Cost" base.
            price = product.with_company(company)._price_compute(
                "standard_price", uom=uom, date=date
            )[product.id]
        return company.currency_id._convert(price, currency, company, date, round=False)

    def _get_oldest_stock_layer(self, product, company):
        """Oldest valuation layer still in stock: the next one a FIFO delivery
        consumes. With the template, any of its variants."""
        variants = (
            product.product_variant_ids
            if product._name == "product.template"
            else product
        )
        return (
            self.env["stock.valuation.layer"]
            .sudo()
            .search(
                [
                    ("product_id", "in", variants.ids),
                    ("company_id", "=", company.id),
                    ("remaining_qty", ">", 0),
                ],
                order="create_date, id",
                limit=1,
            )
        )
