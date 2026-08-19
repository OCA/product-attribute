# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import json

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_matrix(self, product_template):
        order_lines = self.order_line.filtered(
            lambda line: line.product_id
            and line.product_template_id == product_template
        )
        # Check if the secondary_uom_id is the same across all the order lines
        is_same_secondary_uom = all(
            x.secondary_uom_id == order_lines[0].secondary_uom_id for x in order_lines
        )
        # TODO: Improve this case handling
        if not is_same_secondary_uom:
            matrix = super()._get_matrix(product_template)
            matrix.pop("secondary_units", None)
            matrix.pop("secondary_unit_id", None)
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
        secondary_unit = self.env["product.secondary.unit"].browse(
            grid["secondary_unit"] or []
        )
        product_template = self.env["product.template"].browse(
            grid["product_template_id"]
        )
        # The unit selector applies to the whole matrix, so every line of this
        # template gets it, even if its cell wasn't touched.
        self.order_line.filtered(
            lambda x, tmpl=product_template: x.product_template_id == tmpl
        ).secondary_uom_id = secondary_unit
        res = super()._apply_grid()
        if not secondary_unit:
            # Quantities in the matrix are expressed in the main unit of measure,
            # so the standard behavior already did the job.
            return res
        Attrib = self.env["product.template.attribute.value"]
        dirty_cells = grid["changes"]
        for cell in dirty_cells:
            combination = Attrib.browse(cell["ptav_ids"])
            no_variant_attr_values = (
                combination - combination._without_no_variant_attributes()
            )
            # create or find product variant from combination
            product = product_template._create_product_variant(combination)
            order_lines = self.order_line.filtered(
                lambda line,
                product=product,
                no_variant_attr_values=no_variant_attr_values: line.product_id.id
                == product.id
                and line.product_no_variant_attribute_value_ids.ids
                == no_variant_attr_values.ids
            )
            order_lines.secondary_uom_id = secondary_unit
            order_lines.secondary_uom_qty = cell["qty"]
            order_lines._compute_helper_target_field_qty()
        return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    force_product_configurator = fields.Boolean(
        compute="_compute_force_product_configurator"
    )

    @api.depends(
        "product_template_id",
        "order_id.order_line.product_id",
        "order_id.order_line.secondary_uom_id",
    )
    def _compute_force_product_configurator(self):
        """Checks if the order has lines of the same matrix template with different
        secondary units. In that case the matrix can't represent them, so we fall
        back to the regular product configurator."""
        for line in self:
            template = line.product_template_id
            force = False
            if template.product_add_mode == "matrix":
                # Lines without a variant yet (e.g. the placeholder line that opens
                # the configurator) aren't representative of any matrix cell.
                template_lines = line.order_id.order_line.filtered(
                    lambda x, tmpl=template: x.product_id
                    and x.product_template_id == tmpl
                )
                force = len({x.secondary_uom_id.id for x in template_lines}) > 1
            line.force_product_configurator = force

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
