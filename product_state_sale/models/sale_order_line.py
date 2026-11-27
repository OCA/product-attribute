# Copyright 2026 glueckkanja AG
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def _domain_product_id(self):
        return super()._domain_product_id() + [("product_state_can_be_sold", "=", True)]

    @api.constrains("product_id")
    def _check_product_state_can_be_sold(self):
        for line in self:
            product = line.product_id
            if product and not product.product_state_can_be_sold:
                raise ValidationError(
                    self.env._(
                        "Product %(product)s cannot be sold: its state "
                        "%(state)s does not allow sales.",
                        product=product.display_name,
                        state=product.product_state_id.display_name,
                    )
                )
