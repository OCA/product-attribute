# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2019 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models
from odoo.tools import float_compare


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _prepare_sellers(self, params=False):
        """This function is a reimplementation of the builtin-one made for
        `product.product` (variant), excepts that:
        - if override_min_qty is enabled, there is no sort on quantity.
        """
        if self.env.context.get("override_min_qty"):
            return self.seller_ids.filtered(lambda s: s.name.active).sorted(
                lambda s: (s.sequence, s.price, s.id)
            )
        else:
            return self.seller_ids.filtered(lambda s: s.name.active).sorted(
                lambda s: (s.sequence, -s.min_qty, s.price, s.id)
            )

    def _select_seller(
        self, partner_id=False, quantity=0.0, date=None, uom_id=False, params=False
    ):
        """This function is a reimplementation of the builtin-one made for
        `product.product` (variant), excepts that:
        - if product_id (variant) is set, the seller is ignored
        - if override_min_qty is enabled, quantity filtering is ignored
        """
        self.ensure_one()
        if date is None:
            date = fields.Date.context_today(self)
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )

        res = self.env["product.supplierinfo"]
        sellers = self._prepare_sellers(params)
        sellers = sellers.filtered(
            lambda s: not s.company_id or s.company_id.id == self.env.company.id
        )
        for seller in sellers:
            # Set quantity in UoM of seller
            quantity_uom_seller = quantity
            if quantity_uom_seller and uom_id and uom_id != seller.product_uom:
                quantity_uom_seller = uom_id._compute_quantity(
                    quantity_uom_seller, seller.product_uom
                )

            if seller.date_start and seller.date_start > date:
                continue
            if seller.date_end and seller.date_end < date:
                continue
            if partner_id and seller.name not in [partner_id, partner_id.parent_id]:
                continue
            if not self.env.context.get("override_min_qty") and (
                quantity is not None
                and float_compare(
                    quantity_uom_seller, seller.min_qty, precision_digits=precision
                )
                == -1
            ):
                continue
            if seller.product_id:
                continue
            if not res or res.name == seller.name:
                res |= seller
        return res.sorted("price")[:1]

    def price_compute(self, price_type, uom=False, currency=False, company=False):
        """Return dummy not falsy prices when computation is done from supplier
        info for avoiding error on super method. We will later fill these with
        correct values.
        """
        if price_type == "supplierinfo":
            return dict.fromkeys(self.ids, 1.0)
        return super().price_compute(
            price_type, uom=uom, currency=currency, company=company
        )
