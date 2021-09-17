# Copyright 2021 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    item_ids_count = fields.Integer(
        compute="_compute_item_ids_count",
        help="The amount of rule items linked to this pricelist",
    )

    def _get_item_ids_count_domain(self):
        return [("pricelist_id", "in", self.ids)]

    def _compute_item_ids_count(self):
        result = self.env["product.pricelist.item"].read_group(
            self._get_item_ids_count_domain(),
            ["pricelist_id"],
            ["pricelist_id"],
            lazy=True,
        )
        item_dict = {}
        for item in result:
            pricelist_id = item["pricelist_id"][0]
            item_dict.setdefault(pricelist_id, 0)
            item_dict[pricelist_id] += item["pricelist_id_count"]
        for pricelist in self:
            pricelist.item_ids_count = item_dict.get(pricelist.id, 0)

    def show_items(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "product_pricelist_item_button.action_pricelist_item_view"
        )
        action.update(
            {
                "domain": [("pricelist_id", "=", self.id)],
                "name": _("Rules"),
                "target": "current",
            }
        )
        return action
