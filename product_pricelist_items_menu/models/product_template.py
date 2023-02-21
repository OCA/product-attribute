from odoo import fields, models

from ..constants import constants


####################
# Product Template #
####################
class ProductTemplate(models.Model):
    _inherit = "product.template"

    dimension_rule_ids = fields.One2many(
        string="Dimension Rules",
        comodel_name="ooops.dimension.rule",
        inverse_name="product_tmpl_id",
        readonly=True,
        auto_join=False,
    )
    der_ids = fields.Many2many(
        string="Dimension Exclusion Rules",
        readonly=False,
        comodel_name="ooops.dimension.exclusion.rule",
    )

    def _check_dimensions_combination_possible(self, combination):
        dim_vals = {}
        for val in combination:
            dimension = val.attribute_id.dimension
            if dimension:
                att_value_uom_id = val.product_attribute_value_id.uom_id
                if att_value_uom_id:
                    dim_value = att_value_uom_id._compute_quantity(
                        float(self._context.get(dimension, 0)),
                        self.env.ref(constants.DIMENSIONS_BASE_UOM[dimension]),
                    )
                    dim_vals.update({dimension: dim_value})

        if len(dim_vals) > 0:
            dim_vals = constants.check_dim_vals(dim_vals)
            return combination._dimensions_allowed(dim_vals)
        return None

    # -- Check id combination is possible
    def _is_combination_possible(
        self, combination, parent_combination=None, ignore_no_variant=False
    ):
        res = super(ProductTemplate, self)._is_combination_possible(
            combination, parent_combination, ignore_no_variant=ignore_no_variant
        )

        # Proceed only if combination is allowed
        if res:
            possible = self._check_dimensions_combination_possible(combination)
            if possible is not None:
                res = possible

        return res

    def _get_own_attribute_dimension_exclusions(self):
        self.ensure_one()
        product_template_attribute_values = (
            self.valid_product_template_attribute_line_ids.mapped(  # noqa
                "product_template_value_ids"
            )
        )
        return {
            ptav.id: [
                {line_id.dimension: [line_id.value_from, line_id.value_to]}
                for filter_line in ptav.dimension_rule_ids
                for line_id in filter_line.line_ids
            ]
            for ptav in product_template_attribute_values
        }

    def _get_attribute_exclusions(self, parent_combination=None, parent_name=None):
        res = super(ProductTemplate, self)._get_attribute_exclusions(
            parent_combination=parent_combination,
            parent_name=parent_name,
        )

        res["dimensions_exclusions"] = self._get_own_attribute_dimension_exclusions()
        return res

    def write(self, vals):
        new_der_ids = vals.get("der_ids", False)
        new_attribute_line_ids = vals.pop("attribute_line_ids", False)
        if new_attribute_line_ids:
            super(ProductTemplate, self).write(
                {
                    "attribute_line_ids": new_attribute_line_ids,
                }
            )
        for record in self:
            if new_der_ids:
                new_der_ids = new_der_ids[0][2]
                record.env[
                    "ooops.dimension.exclusion.rule"
                ].update_exclusion_rules_for_product_template(new_der_ids, record)
        return super(ProductTemplate, self).write(vals)
