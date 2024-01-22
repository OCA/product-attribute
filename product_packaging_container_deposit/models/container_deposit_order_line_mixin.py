# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class OrderLineMixin(models.AbstractModel):
    """
    Provide common features to order lines.
    Supported order lines: purchase.order.line, sale.order.line.
    """

    _name = "container.deposit.order.line.mixin"
    _description = "Container Deposit Order Line Mixin"

    is_container_deposit = fields.Boolean()

    def _get_product_qty_field(self):
        raise NotImplementedError()

    def _get_product_qty_delivered_received_field(self):
        raise NotImplementedError()

    def _get_order_lines_container_deposit_quantities(self):
        """Get container deposit quantities by product.

        :return: a dict with quantity of container deposit

            {
                container_deposit_product: [quantity, quantity_delivered_received]
            }
        """
        deposit_product_qties = {}
        for line in self:
            line_deposit_qties = (
                line.product_id.get_product_container_deposit_quantities(
                    line[self._get_product_qty_field()],
                    forced_packaging=line.product_packaging_id,
                )
            )
            line_deposit_dlvd_rcvd_qties = (
                line.product_id.get_product_container_deposit_quantities(
                    line[self._get_product_qty_delivered_received_field()],
                    forced_packaging=line.product_packaging_id,
                )
            )

            for plevel in line_deposit_qties:
                product = line_deposit_qties[plevel][0]
                qty = line_deposit_qties[plevel][1]
                if qty == 0:
                    continue
                if plevel in line_deposit_dlvd_rcvd_qties:
                    dlvd_rcvd = line_deposit_dlvd_rcvd_qties[plevel][1]
                else:
                    dlvd_rcvd = 0
                if product in deposit_product_qties:
                    deposit_product_qties[product][0] += qty
                    deposit_product_qties[product][1] += dlvd_rcvd
                else:
                    deposit_product_qties[product] = [qty, dlvd_rcvd]
        return deposit_product_qties

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        if not self.env.context.get(
            "skip_update_container_deposit"
        ) and not self.env.context.get("from_copy"):
            orders = lines.mapped("order_id")
            orders.update_order_container_deposit_quantity()
        return lines

    def write(self, vals):
        res = super().write(vals)
        # Context var to avoid recursive calls when updating container deposit
        if not self.env.context.get("skip_update_container_deposit") and (
            self._get_product_qty_field() in vals
            or self._get_product_qty_delivered_received_field() in vals
        ):
            self.order_id.update_order_container_deposit_quantity()
        return res
