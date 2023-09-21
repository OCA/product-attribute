# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command, models


class OrderMixin(models.AbstractModel):
    """This mixin should only be inherited by purchase.order and sale.order models."""

    _name = "container.deposit.order.mixin"
    _description = "Container Deposit Order Mixin"

    def prepare_deposit_container_line(self, product, qty):
        self.ensure_one()
        values = {
            "name": product.name,
            "product_id": product.id,
            self.order_line._get_product_qty_field(): qty,
            "is_container_deposit": True,
            "order_id": self.id,
            # Bottom of the order
            "sequence": 999,
        }
        return values

    def _get_order_line_field(self):
        raise NotImplementedError()

    def update_order_container_deposit_quantity(self):
        if self.env.context.get("skip_update_container_deposit"):
            return
        self = self.with_context(skip_update_container_deposit=True)
        for order in self:
            # Lines to compute container deposit
            lines_to_comp_deposit = order[self._get_order_line_field()].filtered(
                lambda ln: (
                    ln.product_packaging_id.package_type_id.container_deposit_product_id
                )
                or ln.product_id.packaging_ids
            )
            deposit_container_qties = (
                lines_to_comp_deposit._get_order_lines_container_deposit_quantities()
            )
            for line in self[self._get_order_line_field()]:
                if not line.is_container_deposit:
                    continue
                qty, qty_dlvd_rcvd = deposit_container_qties.pop(
                    line["product_id"], [False, False]
                )
                if not qty:
                    if order.state == "draft":
                        line.unlink()
                    else:
                        line.write(
                            {
                                line._get_product_qty_field(): 0,
                            }
                        )
                else:
                    line.write(
                        {
                            line._get_product_qty_field(): qty,
                            line._get_product_qty_delivered_received_field(): qty_dlvd_rcvd,
                        }
                    )
            values_lst = []
            for product in deposit_container_qties:
                if deposit_container_qties[product][0] > 0:
                    values = order.prepare_deposit_container_line(
                        product, deposit_container_qties[product][0]
                    )
                    values_lst.append(Command.create(values))
            order.write({self._get_order_line_field(): values_lst})

    def copy(self, default=None):
        return super(
            OrderMixin, self.with_context(skip_update_container_deposit=True)
        ).copy(default=default)
