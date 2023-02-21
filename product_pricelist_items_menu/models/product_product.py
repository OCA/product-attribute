from odoo import api, models
from odoo.tools import float_round

from ..constants import constants


class Product(models.Model):
    _inherit = "product.product"

    def get_dim_vals(self):
        ctx = self.env.context
        dim_vals = {}
        for context_key in ctx.keys():
            if context_key in constants.LIST_OF_DIMENSIONS_TO_SEARCH_IN_CONTEXT:
                dim_vals[context_key] = ctx.get(context_key, 0)
        if "default_product_custom_attribute_line_ids" in ctx:
            attribute_values_data = {
                item[2]["attribute_value_id"]: item[2]
                for item in ctx["default_product_custom_attribute_value_ids"]
            }
            custom_value_ids = [key for key in attribute_values_data.keys()]
            attribute_values = self.env["product.attribute.value"].browse(
                custom_value_ids
            )
            for attr_value in attribute_values:
                dimension = attr_value.attribute_id.dimension
                if dimension:
                    value = attribute_values_data[attr_value.id]["custom_value"]
                    if isinstance(value, str):
                        try:
                            value = float(value)
                        except ValueError:
                            value = value
                    dim_vals[dimension] = value
        dim_vals = constants.check_dim_vals(dim_vals)
        return dim_vals

    def check_dim_vals(self, dim_vals):
        """

        :param dim_vals:
        :return:
        """
        if all(
            [
                dim_val not in dim_vals
                for dim_val in constants.LIST_OF_DIMENSIONS_TO_SEARCH_IN_CONTEXT
            ]
        ):
            return False
        return True

    def get_no_variant_ptav_elements(self):
        """
        :return:
        """
        no_variant_ptav_ctx = self._context.get(
            "default_product_no_variant_attribute_value_ids", False
        )
        if no_variant_ptav_ctx:
            no_variant_ptav_ids = [val[1] for val in no_variant_ptav_ctx]
            no_variant_ptav = self.env["product.template.attribute.value"].search(
                [
                    (
                        "id",
                        "in",
                        no_variant_ptav_ids,
                    ),
                    ("attribute_id.dimension", "!=", True),
                ]
            )
        else:
            no_variant_ptav = self.env["product.template.attribute.value"]

        return no_variant_ptav_ctx, no_variant_ptav

    # -- Compute extra price
    @api.depends("product_tmpl_id")
    def _compute_product_price_extra(self):
        dim_vals = self.get_dim_vals()
        if not self.check_dim_vals(dim_vals):
            return super(Product, self)._compute_product_price_extra()

        # Due to the fact that this code works in several scenarios, we need to
        # find the required line in the context for each of them.
        # For one of them, we use custom_key
        # Get no variant ptav ids from context
        no_variant_ptav_ctx, no_variant_ptav = self.get_no_variant_ptav_elements()
        for record_id in self:
            self.calculate_record_price_extra(
                no_variant_ptav_ctx, no_variant_ptav, dim_vals, record_id
            )

    def calculate_record_price_extra(
        self, no_variant_ptav_ctx, no_variant_ptav, dim_vals, record_id
    ):
        """
        :param no_variant_ptav:
        :param dim_vals:
        :param record_id:
        :param no_variant_ptav_ctx:
        :return:
        """
        price_extra = 0
        # Add extra price for "never" ptavs
        for attr in no_variant_ptav.with_context(dim_vals=dim_vals):
            price_extra += attr.price_extra
        # Add extra price for product ptavs
        for attr in record_id.product_template_attribute_value_ids.with_context(
            dim_vals=dim_vals
        ):
            price_extra += attr.price_extra
        price_extra_dimensions = self._compute_dimension_price(
            record_id.product_tmpl_id, dim_vals
        )
        if no_variant_ptav_ctx:
            price_extra = price_extra - sum(
                self._context.get("no_variant_attributes_price_extra", [0])
            )
        record_id.price_extra = price_extra + price_extra_dimensions

    # -- Compute dimension price
    @api.model
    def _compute_dimension_price(self, product_tmpl_id, dimensions, combination=False):
        """
        Compute extra price based on product dimensions
        :param product.template() product_tmpl_id: Product Template
        :type dict{"dimension": value} dimensions: Dict of dimensional values
         (e.g. {"product_length":102.2}
        :return: Float price_extra: Extra price
        """
        extra_price_rules = product_tmpl_id.dimension_rule_ids.filtered(
            lambda r: not r.product_tmpl_attribute_value_id
        )
        for rule in extra_price_rules:
            result = self._check_rule(rule, dimensions)
            if result:
                if combination:
                    result += sum(combination.mapped("price_extra"))
                return result
        return 0

    # -- Compute dimension price
    @api.model
    def _check_rule(self, rule, dimensions):
        """
        Compute extra price based on product dimensions
        :param ooops.dimension.rule() rule: Dimension Rule
        :type dict{"dimension": value} dimensions: Dict of dimensional values
         (e.g. {"product_length":102.2}
        :return: Float price_extra: Extra price for rule
        """
        rule_matched = True
        for line in rule.line_ids:
            if not constants.match_value(
                dimensions[line.dimension], line.value_from, line.value_to
            ):
                rule_matched = False
        if rule_matched:
            price_type = rule.price_type
            if (
                not price_type or price_type == constants.FIXED_PRICE_TYPE
            ):  # Fixed price
                price_extra = rule.price_extra
            else:  # Based on dimension
                dim_value = dimensions[price_type]
                price_extra = dim_value * rule.price_extra
                price_surcharge = rule.price_surcharge
                if not price_surcharge == 0:
                    price_extra += price_surcharge
                if rule.price_round:
                    price_extra = float_round(
                        price_extra, precision_rounding=rule.price_round
                    )
            return price_extra
        else:
            return 0
