# Copyright 2026 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    value_merge_count = fields.Integer(
        compute="_compute_value_merge_count", groups="product.group_product_manager"
    )

    def _compute_value_merge_count(self):
        groups = self.env["product.attribute.value.merge"]._read_group(
            [("attribute_id", "in", self.ids)], ["attribute_id"], ["__count"]
        )
        counts = {attribute.id: count for attribute, count in groups}
        for attribute in self:
            attribute.value_merge_count = counts.get(attribute.id, 0)

    def action_find_duplicate_values(self):
        self.ensure_one()
        finder = self.env["product.attribute.value.merge.finder"].create(
            {"attribute_id": self.id}
        )
        return finder.action_search()

    def action_view_value_merges(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "product_attribute_value_merge.product_attribute_value_merge_action"
        )
        action["domain"] = [("attribute_id", "=", self.id)]
        return action
