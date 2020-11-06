# Copyright 2020 Versada UAB
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    allowed_attribute_ids = fields.One2many(
        comodel_name="product.attribute",
        compute="_compute_allowed_attribute_ids",
        string="Allowed Attributes",
    )
    allowed_attribute_value_ids = fields.One2many(
        comodel_name="product.attribute.value",
        compute="_compute_allowed_attribute_value_ids",
        string="Allowed Attribute Values",
    )
    attribute_id = fields.Many2one(
        domain="""[
            ("id", "in", allowed_attribute_ids),
        ] if allowed_attribute_ids else []""",
    )
    value_ids = fields.Many2many(
        domain="""[
            ("id", "in", allowed_attribute_value_ids),
        ] if allowed_attribute_value_ids else [
            ("attribute_id", "=", attribute_id),
        ]""",
    )

    @api.depends("product_tmpl_id.categ_id")
    def _compute_allowed_attribute_ids(self):
        for rec in self:
            rec.allowed_attribute_ids = (
                rec.product_tmpl_id.categ_id.attribute_line_ids.mapped("attribute_id")
            )

    @api.depends("product_tmpl_id.categ_id", "attribute_id")
    def _compute_allowed_attribute_value_ids(self):
        for rec in self:
            if rec.attribute_id:
                rec.allowed_attribute_value_ids = (
                    rec.product_tmpl_id.categ_id.attribute_line_ids.filtered(
                        lambda al: al.attribute_id == rec.attribute_id
                    ).mapped("value_ids")
                )
            else:
                rec.allowed_attribute_value_ids = False
