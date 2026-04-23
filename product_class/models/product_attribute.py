# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    classes_count = fields.Integer(
        string="Product Classes Count",
        compute="_compute_classes_count",
    )

    class_attribute_line_ids = fields.One2many(
        comodel_name="product.class.attribute.line",
        inverse_name="attribute_id",
        string="Class Attribute Lines",
        help="Product classes that include this attribute.",
    )

    @api.depends("class_attribute_line_ids.class_id")
    def _compute_classes_count(self):
        for attribute in self:
            attribute.classes_count = len(attribute.class_attribute_line_ids.class_id)

    def action_open_product_classes(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "product_class.product_class_action"
        )
        action["domain"] = [("id", "in", self.class_attribute_line_ids.class_id.ids)]
        return action
