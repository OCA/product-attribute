# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductMergeWizardLine(models.TransientModel):

    _name = "product.merge.wizard.line"
    _description = "Merge Products Wizard Line"

    wizard_id = fields.Many2one(
        "product.merge.wizard", string="Wizard", required=True, ondelete="cascade"
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
        ondelete="cascade",
    )
    attribute_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        string="Attribute Values",
        domain="attribute_value_domain",
    )
    attribute_value_domain = fields.Binary(compute="_compute_attribute_value_domain")

    @api.depends("wizard_id.attribute_ids", "wizard_id.line_ids.attribute_value_ids")
    def _compute_attribute_value_domain(self):
        for rec in self:
            rec.attribute_value_domain = [
                ("attribute_id", "in", rec.wizard_id.attribute_ids.ids)
            ]
