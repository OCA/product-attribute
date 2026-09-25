# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    price_ids = fields.One2many(
        comodel_name="product.multi.price",
        inverse_name="product_id",
        string="Other Prices",
        index=True,
    )

    # Read through the record cache: one query for all the products priced
    # together. It holds the prices of every company, so it is only read with
    # sudo, and its cache never holds a list filtered by record rules.
    all_multi_price_ids = fields.One2many(
        comodel_name="product.multi.price",
        inverse_name="product_id",
        string="All Other Prices",
        readonly=True,
        groups="base.group_system",
    )

    def _get_multiprice_base_price(self, rule, date=None):
        """Return the multi price of the price name of ``rule``, or 0."""
        self.ensure_one()
        company = rule.company_id or self.env.user.company_id
        return (
            self.sudo()
            .all_multi_price_ids.filtered(
                lambda p: p.company_id == company and p.name == rule.multi_price_name
            )
            .price
            or 0
        )

    def price_compute(
        self, price_type, uom=None, currency=None, company=None, date=False
    ):
        """Return temporary prices when computation is done for multi price for
        avoiding error on super method. We will later fill these with the
        correct values.
        """
        if price_type == "multi_price":
            return dict.fromkeys(self.ids, 1.0)
        return super().price_compute(
            price_type, uom=uom, currency=currency, company=company, date=date
        )

    @api.model
    def get_views(self, views, options=None):
        if self.user_has_groups("product_multi_price.group_show_multi_prices"):
            self = self.with_context(group_show_multi_prices=True)
        return super(ProductProduct, self).get_views(views, options)
