# Copyright 2023-2026 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import itertools

from odoo import api, fields, models


class AttributeValueDependentMixin(models.AbstractModel):
    _name = "attribute.value.dependent.mixin"
    _description = "Attribute Value Dependent Mixin"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
    )
    available_product_domain = fields.Binary(
        compute="_compute_available_product_domain",
    )
    attribute_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        string="Attribute Values",
    )
    available_attribute_value_domain = fields.Binary(
        compute="_compute_available_attribute_value_domain",
    )

    @api.depends("product_tmpl_id.product_variant_ids")
    def _compute_available_product_domain(self):
        for rec in self:
            if rec.product_tmpl_id:
                rec.available_product_domain = [
                    ("id", "in", rec.product_tmpl_id.product_variant_ids.ids)
                ]
            else:
                rec.available_product_domain = []

    @api.depends("product_tmpl_id.attribute_line_ids.value_ids")
    def _compute_available_attribute_value_domain(self):
        for rec in self:
            if rec.product_tmpl_id:
                rec.available_attribute_value_domain = [
                    ("id", "in", rec.product_tmpl_id.attribute_line_ids.value_ids.ids)
                ]
            else:
                rec.available_attribute_value_domain = []

    def is_matching_product(self, product):
        self.ensure_one()
        if self.product_id:
            return self.product_id == product
        if self.product_tmpl_id and self.product_tmpl_id != product.product_tmpl_id:
            return False
        if self.attribute_value_ids:
            ptav = product.product_template_attribute_value_ids
            attr2vals = {
                attribute: set(values)
                for attribute, values in itertools.groupby(
                    self.attribute_value_ids, lambda pav: pav.attribute_id
                )
            }
            for attribute in attr2vals:
                if attribute not in ptav.attribute_id:
                    return False
                if not attr2vals[attribute] & set(ptav.product_attribute_value_id):
                    return False
        return True
