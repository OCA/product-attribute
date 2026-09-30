from odoo import _, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        """
        Override the standard 'Confirm' button for Purchase Orders.

        Before confirming the order, check if any product in the order lines
        is in a state that is not authorized to be bought.

        Raises:
            ValidationError: If at least one product is not authorized to be bought.
        """
        self._check_order_contain_not_allowed_products()
        return super().button_confirm()

    def _check_order_contain_not_allowed_products(self):
        """
        Check all products in the order lines to ensure they are allowed for purchase.

        Loops through each order and filters lines where the product's
        state has 'authorized_to_be_bought' set to False.

        Raises:
            ValidationError: If any product is in a state that prevents purchase.
        """
        for order in self:
            forbidden_products = order.order_line.filtered(
                lambda line: (
                    line.product_id
                    and line.product_id.product_state_id
                    and not line.product_id.product_state_id.authorized_to_be_bought
                )
            )

            if forbidden_products:
                raise ValidationError(
                    _(
                        "The status of one of the products prevents order "
                        "validation. Please change the product status or "
                        "request a user with the necessary permissions."
                    )
                )
