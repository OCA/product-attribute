# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.exceptions import UserError


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

    def _get_related_fields_variant_template(self):
        res = super()._get_related_fields_variant_template()
        return res + [
            "nutritional_value_ids",
            "nutritional_reference_uom",
            "nutritional_reference_qty",
        ]

    @api.depends("product_variant_ids.nutritional_value_ids")
    def _compute_nutritional_value_ids(self):
        self._compute_template_field_from_variant_field("nutritional_value_ids")

    def _inverse_nutritional_value_ids(self):
        self._set_product_variant_field("nutritional_value_ids")

    @api.depends("product_variant_ids.nutritional_reference_uom")
    def _compute_nutritional_reference_uom(self):
        self._compute_template_field_from_variant_field("nutritional_reference_uom")

    def _inverse_nutritional_reference_uom(self):
        self._set_product_variant_field("nutritional_reference_uom")

    @api.depends("product_variant_ids.nutritional_reference_qty")
    def _compute_nutritional_reference_qty(self):
        self._compute_template_field_from_variant_field("nutritional_reference_qty")

    def _inverse_nutritional_reference_qty(self):
        self._set_product_variant_field("nutritional_reference_qty")

    @api.constrains("nutritional_value_ids")
    def _check_nutritional_type_not_repeated(self):
        for prod in self:
            if prod.nutritional_value_ids and len(prod.nutritional_value_ids) != len(
                prod.nutritional_value_ids.type_id
            ):
                raise UserError(
                    self.env._("Repeating types of nutritional values is not allowed.")
                )
