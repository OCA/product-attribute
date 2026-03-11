# Copyright 2026 APSL-Nagarro Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductPricelistItemHistory(models.Model):
    _name = "product.pricelist.item.history"
    _description = "Pricelist Item Price History"
    _order = "change_date desc"

    product_id = fields.Many2one(
        "product.product", string="Product", readonly=True, required=True
    )
    pricelist_id = fields.Many2one(
        "product.pricelist", string="Pricelist", readonly=True, required=True
    )
    old_price = fields.Float(readonly=True)
    new_price = fields.Float(readonly=True)
    change_date = fields.Datetime(default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one(
        "res.users", string="User", default=lambda self: self.env.user, readonly=True
    )
    active = fields.Boolean(default=True)

    def action_open_label_layout(self):
        products = self.mapped("product_id")
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "product.action_open_label_layout"
        )
        action["context"] = {"default_product_ids": products.ids}
        return action
