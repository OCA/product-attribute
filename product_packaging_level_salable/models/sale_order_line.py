# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, models
from odoo.exceptions import ValidationError


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

    @api.depends("product_id", "product_uom_qty", "product_uom")
    def _compute_product_packaging_id(self):
        res = super()._compute_product_packaging_id()
        for line in self:
            if line.product_packaging_id and not line.product_packaging_id.sales:
                line.product_packaging_id = False
        return res
