# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import _, api, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _can_be_sold_error_condition(self):
        self.ensure_one()
        return self.product_packaging_id and not self.product_packaging_id.sales

    @api.constrains("product_packaging_id")
    def _check_product_packaging_can_be_sold(self):
        for line in self:
            if line._can_be_sold_error_condition():
                raise ValidationError(
                    _(
                        "Packaging %(packaging)s on product %(product)s must be"
                        " set as 'Sales' in order to be used on a sale order."
                    )
                    % {
                        "packaging": line.product_packaging_id.name,
                        "product": line.product_id.name,
                    }
                )

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id(self):
        if self._can_be_sold_error_condition():
            return {
                "warning": {
                    "title": _("Warning"),
                    "message": _(
                        "This product packaging must be set as 'Sales' in"
                        " order to be used on a sale order."
                    ),
                },
            }
        return super()._onchange_product_packaging_id()

    @api.depends("product_id", "product_uom_qty", "product_uom")
    def _compute_product_packaging_id(self):
        res = super()._compute_product_packaging_id()
        for line in self:
            if line.product_packaging_id and not line.product_packaging_id.sales:
                line.product_packaging_id = False
        return res
