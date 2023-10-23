# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import _, api, models
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _can_be_purchased_error_condition(self):
        self.ensure_one()
        return (
            self.product_packaging_id and not self.product_packaging_id.can_be_purchased
        )

    @api.constrains("product_packaging_id")
    def _check_product_packaging_can_be_purchased(self):
        errors = []
        for line in self:
            if line._can_be_purchased_error_condition():
                errors.append(
                    _(
                        "Packaging %(packaging)s on product %(product)s must be"
                        " set as 'Can be purchased' in order to be used on a purchase order."
                    )
                    % {
                        "packaging": line.product_packaging_id.name,
                        "product": line.product_id.name,
                    }
                )
        if errors:
            raise ValidationError("\n".join(errors))

    @api.onchange("product_packaging_id")
    def _onchange_product_packaging_id(self):
        if self._can_be_purchased_error_condition():
            return {
                "warning": {
                    "title": _("Warning"),
                    "message": _(
                        "This product packaging must be set as 'Can be purchased' in"
                        " order to be used on a purchase order."
                    ),
                },
            }
        return super()._onchange_product_packaging_id()

    @api.depends("product_id", "product_uom_qty", "product_uom")
    def _compute_product_packaging_id(self):
        res = super()._compute_product_packaging_id()
        for line in self:
            if (
                line.product_packaging_id
                and not line.product_packaging_id.can_be_purchased
            ):
                line.product_packaging_id = False
        return res
