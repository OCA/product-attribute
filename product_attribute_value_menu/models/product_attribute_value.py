# Copyright 2022 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    product_count = fields.Integer(string="Product", compute="_compute_product_count")

    def _compute_product_count(self):
        for value in self:
            value.product_count = len(value.pav_attribute_line_ids)

    def action_view_product(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "product.product_template_action"
        )
        products = self.pav_attribute_line_ids.mapped("product_tmpl_id")

        if len(products) > 1:
            action["domain"] = [("id", "in", products.ids)]
        elif products:
            form_view = [
                (self.env.ref("product.product_template_only_form_view").id, "form")
            ]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = products.id
        action["context"] = self.env.context
        return action
