# Copyright 2023 Akretion (https://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
from collections import defaultdict

from odoo import api, fields, models


class ProductAttributeRule(models.Model):
    _name = "product.attribute.rule"
    _description = "Product Attribute Rule"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
        required=True,
        ondelete="cascade",
    )

    product_attribute_value_precondition_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        relation="product_attribute_rule_precondition_rel",
        string="Rule preconditions",
        help="This rule will only be applied if all the preconditions are met.\n"
        "The attribute values are ANDed together except if they are from the "
        "same attribute in which case they are ORed.\n"
        "If empty, the rule will always be applied.",
    )

    type = fields.Selection(
        [
            ("only", "Only With"),
            ("never", "Never With"),
        ],
        string="Type",
        default="only",
        required=True,
    )

    product_attribute_value_postcondition_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        relation="product_attribute_rule_postcondition_rel",
        string="Rule postconditions",
        help="The product variant will exist only if these conditions are met "
        "if the precondition is met.\n"
        "The attribute values are ANDed together except if they are from the "
        "same attribute in which case they are ORed.",
        required=True,
    )

    available_precondition_attribute_ids = fields.Many2many(
        comodel_name="product.attribute",
        compute="_compute_available_precondition_attribute_ids",
        string="Available preconditions",
    )

    available_postcondition_attribute_ids = fields.Many2many(
        comodel_name="product.attribute",
        compute="_compute_available_postcondition_attribute_ids",
        string="Available postconditions",
    )

    @api.depends(
        "product_tmpl_id.attribute_line_ids",
        "product_attribute_value_postcondition_ids",
    )
    def _compute_available_precondition_attribute_ids(self):
        """
        Compute the available preconditions.
        """
        for rule in self:
            rule.available_precondition_attribute_ids = (
                rule.product_tmpl_id.attribute_line_ids.mapped("attribute_id")
                - rule.product_attribute_value_postcondition_ids.mapped("attribute_id")
            )

    @api.depends(
        "product_tmpl_id.attribute_line_ids", "product_attribute_value_precondition_ids"
    )
    def _compute_available_postcondition_attribute_ids(self):
        """
        Compute the available postconditions.
        """
        for rule in self:
            rule.available_postcondition_attribute_ids = (
                rule.product_tmpl_id.attribute_line_ids.mapped("attribute_id")
                - rule.product_attribute_value_precondition_ids.mapped("attribute_id")
            )

    def _is_combination_possible(self, combination):
        """
        Check if the combination is possible with the rules defined on the
        product template.
        """
        # Check if the combination matches the preconditions
        if not self._combination_matches_conditions(
            combination, self.product_attribute_value_precondition_ids
        ):
            # If the combination does not match the preconditions,
            # the rule is not applied
            return True

        # Check if the combination matches the postconditions
        match = self._combination_matches_conditions(
            combination, self.product_attribute_value_postcondition_ids
        )

        if self.type == "only" and match:
            # Both conditions are met in only, the combination is possible
            return True
        elif self.type == "never" and not match:
            # Precondition is met but postcondition is not met in never,
            # the combination is possible
            return True

        # The combination is not possible
        return False

    def _combination_matches_conditions(self, combination, conditions):
        """
        Check if the combination matches the given conditions.
        """
        # If there is no condition, the combination matches
        # (only possible for the preconditions)
        if not conditions:
            return True

        # Check if the combination matches the preconditions ANDed between
        # different attributes
        for attribute, attribute_values in self._aggregate_conditions(
            conditions
        ).items():
            if (
                combination.filtered(
                    lambda value: value.attribute_id == attribute
                ).product_attribute_value_id
                not in attribute_values  # The OR between the same attribute values
            ):
                # The combination does not match a precondition
                return False

        # The combination matches all preconditions
        return True

    def _aggregate_conditions(self, conditions):
        """
        Group the attribute values by attribute.
        """
        aggregated_conditions = defaultdict(set)
        for condition in conditions:
            aggregated_conditions[condition.attribute_id].add(condition)

        return aggregated_conditions
