# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
# Copyright 2020 Odoo SA (`_check_pkg_qty_multiple` method)
# License LGPL-3.0 (https://https://www.gnu.org/licenses/lgpl-3.0)

from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_round


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _can_be_sold_error_condition(self):
        self.ensure_one()
        return self.product_packaging_id and not self.product_packaging_id.sales

    def _is_packaging_multiple_check_enabled(self):
        return self.env.company.sale_check_packaging_multiple

    @api.constrains("product_packaging_id")
    def _check_product_packaging_can_be_sold(self):
        for line in self:
            if line._can_be_sold_error_condition():
                raise ValidationError(
                    self.env._(
                        "Packaging %(packaging)s on product %(product)s must be"
                        " set as 'Sales' in order to be used on a sale order.",
                        packaging=line.product_packaging_id.name,
                        product=line.product_id.name,
                    )
                )

    @api.constrains("product_id", "product_packaging_qty", "product_uom_qty")
    def _check_product_packaging_qty_multiple(self):
        if not self._is_packaging_multiple_check_enabled():
            return
        for line in self:
            if not line.product_uom_qty:
                continue
            if error_message_qty_multiple := line._check_pkg_qty_multiple():
                raise ValidationError(error_message_qty_multiple)

    @api.depends("product_id", "product_uom_qty", "product_uom")
    def _compute_product_packaging_id(self):
        res = super()._compute_product_packaging_id()
        for line in self:
            if line.product_packaging_id and not line.product_packaging_id.sales:
                line.product_packaging_id = False
        return res

    def _check_pkg_qty_multiple(self):
        # Ported from sale_stock.models.sale_order_line,_check_package on v14
        default_uom = self.product_id.uom_id
        pack = self.product_packaging_id
        qty = self.product_uom_qty
        q = default_uom._compute_quantity(pack.qty, self.product_uom)
        # We do not use the modulo operator to check if qty is a multiple of q.
        # Indeed the qty per package might be a float, leading to incorrect results.
        # For example: 8 % 1.6 = 1.5999999999999996
        #              5.4 % 1.8 = 2.220446049250313e-16
        if (
            qty
            and q
            and float_compare(
                qty / q,
                float_round(qty / q, precision_rounding=1.0),
                precision_rounding=0.001,
            )
            != 0
        ):
            next_valid_qty = qty - (qty % q) + q
            return self.env._(
                "This product is packaged by %(pack_size).2f %(pack_name)s. "
                + "You should sell %(quantity).2f %(unit)s.",
                pack_size=pack.qty,
                pack_name=default_uom.name,
                quantity=next_valid_qty,
                unit=self.product_uom.name,
            )
