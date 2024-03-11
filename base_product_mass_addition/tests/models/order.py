# Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
# @author Iván Todorovich <ivan.todorovich@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ModelOrder(models.Model):
    _name = "model.order"
    _description = "Test Model Order (base_product_mass_addition)"
    _inherit = "product.mass.addition"

    line_ids = fields.One2many("model.order.line", "order_id")

    def _get_quick_line(self, product):
        return fields.first(
            self.line_ids.filtered(lambda rec: rec.product_id == product)
        )

    def _get_quick_line_qty_vals(self, product):
        return {"product_qty": product.qty_to_process}

    def _complete_quick_line_vals(self, vals, lines_key=""):
        return super()._complete_quick_line_vals(vals, lines_key="line_ids")

    def _add_quick_line(self, product, lines_key=""):
        return super()._add_quick_line(product, lines_key="line_ids")


class ModelOrderLine(models.Model):
    _name = "model.order.line"
    _description = "Test Model Order Line (base_product_mass_addition)"

    order_id = fields.Many2one("model.order")
    product_id = fields.Many2one("product.product")
    product_qty = fields.Float()
