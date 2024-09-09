# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from collections import defaultdict

from odoo import _, api, models
from odoo.osv import expression


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "product.catalog.mixin"]

    def _compute_catalog_button_text(self):
        self.catalog_button_text = _("Back to picking")

    def _get_action_add_from_catalog_extra_context(self):
        return {
            **super()._get_action_add_from_catalog_extra_context(),
            "order_id": self.id,
        }

    def _default_order_line_values(self):
        default_data = super()._default_order_line_values()
        new_default_data = self.env["stock.move"]._get_product_catalog_lines_data()
        return {**default_data, **new_default_data}

    def _get_product_catalog_domain(self):
        return expression.AND(
            [
                super()._get_product_catalog_domain(),
                [("type", "in", ["consu", "product"])],
            ]
        )

    def _get_product_catalog_record_lines(self, product_ids):
        grouped_moves = defaultdict(lambda: self.env["stock.move"])
        for move in self.move_ids:
            if move.product_id.id not in product_ids:
                continue
            grouped_moves[move.product_id] |= move
        return grouped_moves

    @api.model
    def _prepare_stock_move_vals_from_catalog(self, product_id, quantity):
        self.ensure_one()
        product_id = self.env["product.product"].browse(product_id)
        return {
            "name": product_id.display_name,
            "product_id": product_id.id,
            "product_uom_qty": quantity,
            "product_uom": product_id.uom_id.id,
            "location_id": self.location_id.id,
            "location_dest_id": self.location_dest_id.id,
            "picking_id": self.id,
            "state": self.state,
            "picking_type_id": self.picking_type_id.id,
            "restrict_partner_id": self.owner_id.id,
            "company_id": self.company_id.id,
            "partner_id": self.partner_id.id,
            # Put it at the end of the order
            "sequence": ((self.move_ids and self.move_ids[-1].sequence + 1) or 10),
        }

    def _update_order_line_info(self, product_id, quantity, **kwargs):
        """Update stock move information for a given product or create a
        new one if none exists yet.
        :param int product_id: The product, as a `product.product` id.
        :return: There's no price unit so we return always None show nothing is shown
        :rtype: None
        """
        move = self.move_ids.filtered(lambda move: move.product_id.id == product_id)
        if move:
            if quantity != 0:
                move.product_uom_qty = quantity
            elif self.state == "draft":
                move.unlink()
                return None
            else:
                move.product_uom_qty = 0
        elif quantity > 0:
            move = self.env["stock.move"].create(
                self._prepare_stock_move_vals_from_catalog(product_id, quantity)
            )
        return None

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


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_product_catalog_lines_data(self, **kwargs):
        """Return information about sale order lines in `self`.

        If `self` is empty, this method returns only the default value(s) needed for
        the product catalog. In this case, the quantity that equals 0.

        Otherwise, it returns a quantity and a price based on the product of the SOL(s)
        and whether the product is read-only or not.

        A product is considered read-only if the picking is cancelled or done.

        Note: This method cannot be called with multiple records that have different
        products linked.

        :raise odoo.exceptions.ValueError: ``len(self.product_id) != 1``
        :rtype: dict
        :return: A dict with the following structure:
            {
                'quantity': float,
                'readOnly': bool,
            }
        """
        if len(self) == 1:
            res = {
                "quantity": self.product_uom_qty,
                "readOnly": self.picking_id.state in ["cancel", "done"],
            }
            return res
        elif self:
            self.product_id.ensure_one()
            res = {
                "readOnly": True,
                "quantity": sum(
                    self.mapped(
                        lambda move: move.product_uom._compute_quantity(
                            qty=move.product_uom_qty,
                            to_unit=move.product_id.uom_id,
                        )
                    )
                ),
            }
            return res
        else:
            return {
                "quantity": 0,
            }

    def action_add_from_catalog(self):
        picking = self.env["stock.picking"].browse(self.env.context.get("order_id"))
        return picking.action_add_from_catalog()
