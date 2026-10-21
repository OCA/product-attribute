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

    def _filter_combinations_impossible_by_config(
        self, combination_tuples, ignore_no_variant=False
    ):
        """Filter out the combinations excluded by the attribute rules.

        This method is used by ``_create_variant_ids`` to (re)generate the
        variants, and by ``_is_combination_possible_by_config``.
        """
        combinations = super()._filter_combinations_impossible_by_config(
            combination_tuples, ignore_no_variant=ignore_no_variant
        )
        if not self.use_attribute_rules:
            yield from combinations
            return
        for combination in combinations:
            if self._is_combination_possible_with_rules(combination):
                yield combination

    def _is_combination_possible_with_rules(self, combination):
        """
        Check if the combination is possible with the rules defined
        on the product template.
        """
        # Rules are ANDed together
        for rule in self.product_attribute_rule_ids:
            if not rule._is_combination_possible(combination):
                return False
        return True

    def write(self, vals):
        res = super().write(vals)

        # super() already recreates the variants when the attribute lines
        # change or when (re)activating a product that has no variant yet.
        handled_by_super = "attribute_line_ids" in vals or (
            vals.get("active") and not self.product_variant_ids
        )
        rules_updated = (
            "use_attribute_rules" in vals or "product_attribute_rule_ids" in vals
        )
        if rules_updated and not handled_by_super:
            # Recreate the variants according to the updated rules
            self._create_variant_ids()

        return res
