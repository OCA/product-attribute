# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import json

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_matrix(self, product_template):
        order_lines = self.order_line.filtered(
            lambda line: line.product_template_id == product_template
        )
        # Check if the secondary_uom_id is the same across all the order lines
        is_same_secondary_uom = all(
            x.secondary_uom_id == order_lines[0].secondary_uom_id for x in order_lines
        )
        # TODO: Improve this case handling
        if not is_same_secondary_uom:
            matrix = super()._get_matrix(product_template)
            matrix.pop("secondary_units", None)
            return matrix
        # Whether true or false...
        matrix = super(
            SaleOrder,
            self.with_context(
                get_matrix_secondary_unit_id=order_lines.secondary_uom_id
            ),
        )._get_matrix(product_template)
        # There could be a default secondary in unit in which case we'll set it directly
        # TODO: We should be able to flag the lines as already set by the matrix somehow
        # so if there's no secondary unit selected it doesn't default to that default
        # secondary unit every time.
        matrix["secondary_unit_id"] = order_lines.secondary_uom_id.id or (
            not order_lines and matrix.get("secondary_unit_id")
        )
        return matrix

    @api.onchange("grid")
    def _apply_grid(self):
        if not self.grid or not self.grid_update:
            return super()._apply_grid()
        grid = json.loads(self.grid)
        if "secondary_unit" not in grid:
            return super()._apply_grid()
        # In case that only the secondary unit is changed we need to set it manually
        if not grid.get("changed"):
            lines = self.order_line.filtered(
                lambda x, grid_template=self.grid_product_tmpl_id: grid_template
                == x.product_template_id
            )
            lines.secondary_uom_id = self.env["product.secondary.unit"].browse(
                grid["secondary_unit"]
            )
        return super(
            SaleOrder, self.with_context(grid_secondary_unit_id=grid["secondary_unit"])
        )._apply_grid()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    force_product_configurator = fields.Boolean(
        compute="_compute_force_product_configurator"
    )

    @api.depends("secondary_uom_id")
    def _compute_force_product_configurator(self):
        """Checks if there are matrix products with the same template and different
        secondary unit for every order"""
        self.force_product_configurator = False
        for order in self.order_id:
            product_templates = order.order_line.product_template_id.filtered(
                lambda x: x.product_add_mode == "matrix"
            )
            for product_template in product_templates:
                order_lines = order.order_line.filtered(
                    lambda x: x.product_template_id == product_template
                )
                if not all(
                    x.secondary_uom_id == order_lines[0].secondary_uom_id
                    for x in order_lines
                ):
                    self.force_product_configurator = True

    @api.onchange("product_id")
    def product_id_change(self):
        if "grid_secondary_unit_id" not in self.env.context:
            return super().product_id_change()
        secondary_uom_id = self.env.context.get("grid_secondary_unit_id")
        product_uom_qty = self.product_uom_qty
        if not secondary_uom_id:
            self.secondary_uom_qty = False
        res = super(
            SaleOrderLine, self.with_context(skip_secondary_uom_default=True)
        ).product_id_change()
        self.secondary_uom_id = self.env["product.secondary.unit"].browse(
            secondary_uom_id
        )
        if self.secondary_uom_id:
            self.secondary_uom_qty = product_uom_qty
            self.onchange_product_uom_for_secondary()
        else:
            self.product_uom_qty = product_uom_qty
        return res

    def mapped(self, func):
        # HACK: Use secondary_uom_qty when needed to avoid reparsing the matrix
        if (
            self.env.context.get("get_matrix_secondary_unit_id")
            and func
            and isinstance(func, str)
            and func == "product_uom_qty"
        ):
            func = "secondary_uom_qty"
        return super().mapped(func)
