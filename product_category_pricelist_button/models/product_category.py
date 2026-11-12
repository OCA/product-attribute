# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    pricelist_count = fields.Integer(
        compute="_compute_pricelist_count",
        store=True,
        help="The number of pricelists associated with products under this category.",
    )

    pricelist_item_ids = fields.One2many("product.pricelist.item", "categ_id")

    @api.depends("pricelist_item_ids")
    def _compute_pricelist_count(self):
        PricelistItem = self.env["product.pricelist.item"]

        fetch_data = PricelistItem.read_group(
            [("categ_id", "in", self.ids)], ["categ_id"], ["categ_id"]
        )

        for category in self:
            category.pricelist_count = sum(
                data["categ_id_count"]
                for data in fetch_data
                if data["categ_id"][0] == category.id
            )

    def action_view_pricelists(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Pricelists",
            "res_model": "product.pricelist.item",
            "domain": [("categ_id", "in", self.ids)],
            "view_mode": "list,form",
            "target": "current",
        }
