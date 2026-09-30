from odoo import _, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """
        Override the standard confirmation of a Sales Order.

        Before confirming the order, ensure that all products in the order
        lines are allowed to be sold according to their product state.

        Raises:
            ValidationError: If at least one product is not authorized to be sold.
        """
        self._check_order_contain_not_allowed_products()
        return super().action_confirm()

    def _check_order_contain_not_allowed_products(self):
        """
        Validate that all products in the sales order are allowed for sale.

        This method checks each order line and verifies that the related
        product's state has 'authorized_to_be_sold' set to True.

        Raises:
            ValidationError: If any product is in a state that prevents sale.
        """
        for order in self:
            forbidden_products = order.order_line.filtered(
                lambda line: (
                    line.product_id
                    and line.product_id.product_state_id
                    and not line.product_id.product_state_id.authorized_to_be_sold
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
