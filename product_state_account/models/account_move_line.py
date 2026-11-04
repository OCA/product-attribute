# Copyright 2026 glueckkanja AG
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.constrains("product_id", "display_type")
    def _check_product_state_can_be_invoiced(self):
        for line in self:
            product = line.product_id
            if (
                line.display_type == "product"
                and product
                and line.move_id.is_sale_document(include_receipts=True)
                and not product.product_state_can_be_invoiced
            ):
                raise ValidationError(
                    self.env._(
                        "Product %(product)s cannot be invoiced: its state "
                        "%(state)s does not allow invoicing.",
                        product=product.display_name,
                        state=product.product_state_id.display_name,
                    )
                )
