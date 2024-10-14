from collections import defaultdict

from odoo import models
from odoo.osv import expression


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "product.catalog.mixin"]

    def _default_order_line_values(self):
        default_data = super()._default_order_line_values()
        new_default_data = self.env["sale.order.line"]._get_product_catalog_lines_data()
        return {**default_data, **new_default_data}

    def _get_action_add_from_catalog_extra_context(self):
        return {
            **super()._get_action_add_from_catalog_extra_context(),
            "product_catalog_currency_id": self.currency_id.id,
            "product_catalog_digits": self.order_line._fields["price_unit"].get_digits(
                self.env
            ),
        }

    def _get_product_catalog_domain(self):
        return expression.AND(
            [super()._get_product_catalog_domain(), [("sale_ok", "=", True)]]
        )

    def _get_product_catalog_order_data(self, products, **kwargs):
        pricelist = self.pricelist_id._get_products_price(
            quantity=1.0,
            products=products,
            currency=self.currency_id,
            date=self.date_order,
            **kwargs,
        )
        res = super()._get_product_catalog_order_data(products, **kwargs)
        for product in products:
            res[product.id]["price"] = pricelist.get(product.id)
            if product.sale_line_warn != "no-message" and product.sale_line_warn_msg:
                res[product.id]["warning"] = product.sale_line_warn_msg
            if product.sale_line_warn == "block":
                res[product.id]["readOnly"] = True
        return res

    def _get_product_catalog_record_lines(self, product_ids):
        grouped_lines = defaultdict(lambda: self.env["sale.order.line"])
        for line in self.order_line:
            if line.display_type or line.product_id.id not in product_ids:
                continue
            grouped_lines[line.product_id] |= line
        return grouped_lines

    def _update_order_line_info(self, product_id, quantity, **kwargs):
        """Update sale order line information for a given product or create a
        new one if none exists yet.
        :param int product_id: The product, as a `product.product` id.
        :return: The unit price of the product, based on the pricelist of the
                 sale order and the quantity selected.
        :rtype: float
        """
        sol = self.order_line.filtered(lambda line: line.product_id.id == product_id)
        if sol:
            if quantity != 0:
                sol.product_uom_qty = quantity
            elif self.state in ["draft", "sent"]:
                price_unit = self.pricelist_id._get_product_price(
                    product=sol.product_id,
                    quantity=1.0,
                    currency=self.currency_id,
                    date=self.date_order,
                    **kwargs,
                )
                sol.unlink()
                return price_unit
            else:
                sol.product_uom_qty = 0
        elif quantity > 0:
            sol = self.env["sale.order.line"].create(
                {
                    "order_id": self.id,
                    "product_id": product_id,
                    "product_uom_qty": quantity,
                    # Put it at the end of the order
                    "sequence": (
                        (self.order_line and self.order_line[-1].sequence + 1) or 10
                    ),
                }
            )
        return sol.price_unit

    def _is_readonly(self):
        """Return Whether the sale order is read-only or not based on the state or the
        lock status.

        A sale order is considered read-only if its state is 'cancel' or if the sale
        order is locked.

        :return: Whether the sale order is read-only or not.
        :rtype: bool
        """
        self.ensure_one()
        return self.state in ["cancel", "done"]


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_product_catalog_lines_data(self, **kwargs):
        """Return information about sale order lines in `self`.

        If `self` is empty, this method returns only the default value(s) needed for
        the product catalog. In this case, the quantity that equals 0.

        Otherwise, it returns a quantity and a price based on the product of the SOL(s)
        and whether the product is read-only or not.

        A product is considered read-only if the order is considered read-only (see
        ``SaleOrder._is_readonly`` for more details) or if `self` contains multiple
        records or if it has sale_line_warn == "block".

        Note: This method cannot be called with multiple records that have different
        products linked.

        :raise odoo.exceptions.ValueError: ``len(self.product_id) != 1``
        :rtype: dict
        :return: A dict with the following structure:
            {
                'quantity': float,
                'price': float,
                'readOnly': bool,
                'warning': String
            }
        """
        if len(self) == 1:
            res = {
                "quantity": self.product_uom_qty,
                "price": self.price_unit,
                "readOnly": self.order_id._is_readonly()
                or (self.product_id.sale_line_warn == "block"),
            }
            if (
                self.product_id.sale_line_warn != "no-message"
                and self.product_id.sale_line_warn_msg
            ):
                res["warning"] = self.product_id.sale_line_warn_msg
            return res
        elif self:
            self.product_id.ensure_one()
            order_line = self[0]
            order = order_line.order_id
            res = {
                "readOnly": True,
                "price": order.pricelist_id._get_product_price(
                    product=order_line.product_id,
                    quantity=1.0,
                    currency=order.currency_id,
                    date=order.date_order,
                    **kwargs,
                ),
                "quantity": sum(
                    self.mapped(
                        lambda line: line.product_uom._compute_quantity(
                            qty=line.product_uom_qty,
                            to_unit=line.product_id.uom_id,
                        )
                    )
                ),
            }
            if (
                self.product_id.sale_line_warn != "no-message"
                and self.product_id.sale_line_warn_msg
            ):
                res["warning"] = self.product_id.sale_line_warn_msg
            return res
        else:
            # price will be computed in batch with pricelist utils so not given here
            return {
                "quantity": 0,
            }

    def action_add_from_catalog(self):
        order = self.env["sale.order"].browse(self.env.context.get("order_id"))
        return order.action_add_from_catalog()
