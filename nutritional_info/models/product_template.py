# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    nutritional_reference_qty = fields.Float(
        string="Nutritional reference quantity",
        compute="_compute_nutritional_reference_qty",
        inverse="_inverse_nutritional_reference_qty",
    )
    nutritional_reference_uom = fields.Many2one(
        comodel_name="uom.uom",
        compute="_compute_nutritional_reference_uom",
        inverse="_inverse_nutritional_reference_uom",
    )
    nutritional_value_ids = fields.One2many(
        comodel_name="nutritional.value",
        compute="_compute_nutritional_value_ids",
        inverse="_inverse_nutritional_value_ids",
    )

    @api.depends("product_variant_ids.nutritional_value_ids")
    def _compute_nutritional_value_ids(self):
        for template in self:
            if template.product_variant_count == 1:
                variant = template.product_variant_ids
                template.nutritional_value_ids = variant.nutritional_value_ids

    def _inverse_nutritional_value_ids(self):
        for template in self:
            if template.product_variant_count == 1:
                variant = template.product_variant_ids
                variant.nutritional_value_ids = template.nutritional_value_ids

    @api.depends("product_variant_ids.nutritional_reference_uom")
    def _compute_nutritional_reference_uom(self):
        for template in self:
            if template.product_variant_count == 1:
                variant = template.product_variant_ids
                template.nutritional_reference_uom = variant.nutritional_reference_uom

    def _inverse_nutritional_reference_uom(self):
        for template in self:
            if template.product_variant_count == 1:
                variant = template.product_variant_ids
                variant.nutritional_reference_uom = template.nutritional_reference_uom

    @api.depends("product_variant_ids.nutritional_reference_qty")
    def _compute_nutritional_reference_qty(self):
        for template in self:
            if template.product_variant_count == 1:
                variant = template.product_variant_ids
                template.nutritional_reference_qty = variant.nutritional_reference_qty

    def _inverse_nutritional_reference_qty(self):
        for template in self:
            if template.product_variant_count == 1:
                variant = template.product_variant_ids
                variant.nutritional_reference_qty = template.nutritional_reference_qty
