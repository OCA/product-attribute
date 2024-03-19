# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    alternative_pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        string="Alternative pricelists",
        relation="product_pricelist_alternative_rel",
        column1="origin_id",
        column2="alternative_id",
        domain="[('id', '!=', id)]",
    )
    is_alternative_to_pricelist_ids = fields.Many2many(
        comodel_name="product.pricelist",
        string="Is alternative to pricelists",
        relation="product_pricelist_alternative_rel",
        column1="alternative_id",
        column2="origin_id",
    )
    is_alternative_to_pricelist_count = fields.Integer(
        compute="_compute_is_alternative_to_pricelist_count"
    )

    @api.depends("is_alternative_to_pricelist_ids")
    def _compute_is_alternative_to_pricelist_count(self):
        groups = self.read_group(
            [("alternative_pricelist_ids", "in", self.ids)],
            ["alternative_pricelist_ids"],
            "alternative_pricelist_ids",
            lazy=False,
        )
        data = {
            group["alternative_pricelist_ids"][0]: group["__count"] for group in groups
        }
        for pricelist in self:
            pricelist.is_alternative_to_pricelist_count = data.get(pricelist.id, 0)

    def action_view_is_alternative_to_pricelist(self):
        self.ensure_one()
        action = {
            "type": "ir.actions.act_window",
            "name": _("Is Alternative to Pricelist"),
            "res_model": "product.pricelist",
            "view_mode": "tree,form",
            "domain": [("id", "in", self.is_alternative_to_pricelist_ids.ids)],
            "context": dict(self.env.context, create=False),
        }
        if self.is_alternative_to_pricelist_count == 1:
            action.update(
                {"view_mode": "form", "res_id": self.is_alternative_to_pricelist_ids.id}
            )
        return action

    def _compute_price_rule(self, products, qty, uom=None, date=False, **kwargs):
        res = super()._compute_price_rule(products, qty, uom=uom, date=date, **kwargs)
        for product in products:
            reference_pricelist_item = self.env["product.pricelist.item"].browse(
                res[product.id][1]
            )
            if (
                reference_pricelist_item.alternative_pricelist_policy
                == "use_lower_price"
            ):
                for alternative_pricelist in self.alternative_pricelist_ids:
                    alternative_price_rule = alternative_pricelist._compute_price_rule(
                        product, qty, uom=uom, date=date, **kwargs
                    )
                    # use alternative price if lower
                    if alternative_price_rule[product.id][0] < res[product.id][0]:
                        res[product.id] = alternative_price_rule[product.id]
        return res
