# Copyright 2023 Akretion (https://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_attribute_rule_ids = fields.One2many(
        comodel_name="product.attribute.rule",
        inverse_name="product_tmpl_id",
        string="Product Attribute Rules",
    )

    use_attribute_rules = fields.Boolean(
        string="Use Attribute Rules",
        help="If checked, the product variants will be generated based on the rules "
        "defined below.",
    )

    product_attribute_value_ids = fields.Many2many(
        string="Technical Attributes",
        comodel_name="product.attribute.value",
        compute="_compute_product_attribute_value_ids",
    )

    @api.depends("attribute_line_ids.value_ids")
    def _compute_product_attribute_value_ids(self):
        for template in self:
            template.product_attribute_value_ids = template.mapped(
                "attribute_line_ids.value_ids"
            )

    def _is_combination_possible_by_config(self, combination, ignore_no_variant=False):
        rv = super()._is_combination_possible_by_config(
            combination, ignore_no_variant=ignore_no_variant
        )
        if (
            not rv  # Combination is not possible
            or not self.use_attribute_rules  # Rules are not enabled
            or not self.product_attribute_rule_ids  # No rules defined
        ):
            return rv

        # Check if the combination matches the rules
        return self._is_combination_possible_with_rules(combination)

    def _is_combination_possible_with_rules(self, combination):
        """
        Check if the combination is possible with the rules defined on the product template.
        """
        # Rules are ANDed together
        for rule in self.product_attribute_rule_ids:
            if not rule._is_combination_possible(combination):
                return False
        return True

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)

        # Recreate variants if the rules have changed
        empty = vals.get("active") and len(self.product_variant_ids) == 0
        if "attribute_line_ids" in vals or empty:
            # Already done in super
            return res

        if "use_attribute_rules" in vals or "product_attribute_rule_ids" in vals:
            # Recreate variants
            self._create_variant_ids()

        return res
