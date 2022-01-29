# Copyright 2018 Carlos Dauden - Tecnativa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class ProductPricelistItemDuplicateWizard(models.TransientModel):
    _name = "product.pricelist.item.duplicate.wizard"
    _description = "Wizard Product Pricelist Item Duplicate"

    date_start = fields.Date(required=True)
    date_end = fields.Date()
    variation_percent = fields.Float(digits="Product Price", string="Variation %")

    def action_apply(self):
        PricelistItem = self.env["product.pricelist.item"]
        new_items = PricelistItem
        for item in PricelistItem.browse(self.env.context["active_ids"]):
            new_items |= item.copy(
                {
                    "date_start": self.date_start,
                    "date_end": self.date_end,
                    "previous_item_id": item.id,
                    "fixed_price": item.fixed_price
                    * (1.0 + self.variation_percent / 100.0),
                }
            )
            item.date_end = self.date_start - relativedelta(days=1)

        xmlid = "product_pricelist_revision.product_pricelist_item_action"
        action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
        if len(new_items) > 0:
            action["domain"] = [("id", "in", new_items.ids)]
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action
