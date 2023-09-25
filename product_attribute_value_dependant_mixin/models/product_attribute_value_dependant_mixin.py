# Copyright 2023 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json

from odoo import api, fields, models


class AttributeValueDependantMixin(models.AbstractModel):
    _name = "attribute.value.dependant.mixin"
    _description = "Attribute Value Dependant Mixin"

    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
    )
    attribute_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        string="Attribute Values",
        domain="[('id', 'in', available_attribute_value_ids)]",
    )
    available_attribute_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        string="Available Attribute Values",
        compute="_compute_available_attribute_value_ids",
    )
    available_attribute_value_domain = fields.Char(
        compute="_compute_available_attribute_value_domain",
    )

    @api.depends(
        "product_tmpl_id",
        "product_tmpl_id.attribute_line_ids.value_ids",
        "available_attribute_value_domain",
    )
    def _compute_available_attribute_value_ids(self):
        for rec in self:
            if rec.product_tmpl_id:
                rec.available_attribute_value_ids = rec.product_tmpl_id.mapped(
                    "attribute_line_ids.value_ids"
                ).filtered_domain(json.loads(rec.available_attribute_value_domain))
            else:
                rec.available_attribute_value_ids = None

    @api.depends("product_tmpl_id", "product_tmpl_id.attribute_line_ids.value_ids")
    def _compute_available_attribute_value_domain(self):
        for rec in self:
            domain = []
            if rec.product_tmpl_id:
                domain = [
                    ("id", "in", rec.product_tmpl_id.attribute_line_ids.value_ids.ids)
                ]
            rec.available_attribute_value_domain = json.dumps(domain)
