# Copyright 2023 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from functools import partial

from odoo import Command, _, models

_logger = logging.getLogger(__name__)


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
        self = self.with_context(
            skip_update_container_deposit=True,
            update_order_container_deposit_quantity=True,
        )
        line_ids_to_delete = []
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
            values_lst = []
            for line in self[self._get_order_line_field()]:
                if not line.is_container_deposit:
                    continue
                qty, qty_dlvd_rcvd = deposit_container_qties.pop(
                    line["product_id"], [False, False]
                )
                if not qty:
                    new_vals = {
                        line._get_product_qty_field(): 0,
                    }
                    if order.state == "draft":
                        # values_lst.append(Command.delete(line.id))
                        line_ids_to_delete.append(line.id)
                        # TODO: check if it is needed for UI only
                        new_vals["name"] = _("[DEL] %(name)s", name=line.name)
                    # else:
                    values_lst.append(
                        Command.update(
                            line.id,
                            new_vals,
                        )
                    )

                else:
                    values_lst.append(
                        Command.update(
                            line.id,
                            {
                                line._get_product_qty_field(): qty,
                                line._get_product_qty_delivered_received_field(): qty_dlvd_rcvd,
                            },
                        )
                    )
            for product in deposit_container_qties:
                if deposit_container_qties[product][0]:
                    values = order.prepare_deposit_container_line(
                        product, deposit_container_qties[product][0]
                    )
                    values_lst.append(Command.create(values))
            order.write({self._get_order_line_field(): values_lst})
        # Schedule line to delete after commit to avoid caching issue w/ UI
        if line_ids_to_delete:
            self.env.cr.postcommit.add(
                partial(
                    self._order_container_deposit_delete_lines_after_commit,
                    sorted(line_ids_to_delete),
                )
            )

    def _order_container_deposit_delete_lines_after_commit(self, line_ids):
        line_model = self._fields[self._get_order_line_field()].comodel_name
        recs = self.env[line_model].browse(line_ids).exists()
        recs.unlink()
        _logger.debug("%s deleted after commit", recs)
        # Needs an explicit commit as it runs after the original commit is done
        self.env.cr.commit()  # pylint: disable=invalid-commit

    def copy(self, default=None):
        return super(
            OrderMixin, self.with_context(skip_update_container_deposit=True)
        ).copy(default=default)
