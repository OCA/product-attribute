# Copyright 2018 Carlos Dauden - Tecnativa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class ProductPricelistItemDuplicateWizard(models.TransientModel):
    _name = "product.pricelist.item.duplicate.wizard"
    _description = "Wizard Product Pricelist Item Duplicate"

    pricelist_id = fields.Many2one(
        comodel_name="product.pricelist",
        help="When set, all the fixed price items of this pricelist that are "
        "still valid at the start date are revised.",
    )
    categ_id = fields.Many2one(
        comodel_name="product.category",
        string="Product Category",
        help="Only revise the items of products in this category "
        "(child categories included).",
    )
    date_start = fields.Datetime(required=True)
    date_end = fields.Datetime()
    variation_percent = fields.Float(digits="Product Price", string="Variation %")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        ctx = self.env.context
        if (
            "pricelist_id" in fields_list
            and ctx.get("active_model") == "product.pricelist"
            and ctx.get("active_id")
        ):
            res["pricelist_id"] = ctx["active_id"]
        return res

    def _get_pricelist_items_domain(self):
        self.ensure_one()
        domain = [
            ("pricelist_id", "=", self.pricelist_id.id),
            ("compute_price", "=", "fixed"),
            "|",
            ("date_start", "=", False),
            ("date_start", "<", self.date_start),
            "|",
            ("date_end", "=", False),
            ("date_end", ">=", self.date_start),
        ]
        if self.categ_id:
            domain += [
                "|",
                "|",
                ("categ_id", "child_of", self.categ_id.id),
                ("product_tmpl_id.categ_id", "child_of", self.categ_id.id),
                ("product_id.categ_id", "child_of", self.categ_id.id),
            ]
        return domain

    def _get_items_to_revise(self):
        """Return (items to revise, number of skipped items)."""
        self.ensure_one()
        PricelistItem = self.env["product.pricelist.item"]
        if self.pricelist_id:
            return PricelistItem.search(self._get_pricelist_items_domain()), 0
        items = PricelistItem.browse(self.env.context.get("active_ids", []))
        to_revise = items.filtered(lambda i: i.compute_price == "fixed")
        return to_revise, len(items - to_revise)

    def action_apply(self):
        self.ensure_one()
        items, skipped = self._get_items_to_revise()
        if not items:
            raise UserError(self.env._("There are no fixed price items to revise."))
        new_items = self.env["product.pricelist.item"]
        for item in items:
            new_items |= item.copy(
                {
                    "date_start": self.date_start,
                    "date_end": self.date_end,
                    "previous_item_id": item.id,
                    "fixed_price": item.fixed_price
                    * (1.0 + self.variation_percent / 100.0),
                }
            )
            item.date_end = self.date_start - relativedelta(seconds=1)

        xmlid = "product_pricelist_revision.product_pricelist_item_action"
        action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
        action["context"] = {}
        action["domain"] = [("id", "in", new_items.ids)]
        if skipped:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "type": "warning",
                    "message": self.env._(
                        "%(skipped)s item(s) were skipped because they are not "
                        "fixed price items.",
                        skipped=skipped,
                    ),
                    "next": action,
                },
            }
        return action
