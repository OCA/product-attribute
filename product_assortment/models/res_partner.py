# Copyright 2021 Tecnativa - Carlos Roca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def action_define_product_assortment(self):
        self.ensure_one()
        xmlid = "product_assortment.actions_product_assortment_view"
        action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
        action["domain"] = [
            ("partner_ids", "in", self.ids),
            ("is_assortment", "=", True),
        ]
        ctx = self.env.context.copy()
        ctx.update(
            {
                "default_partner_ids": self.ids,
                "default_is_assortment": True,
                "product_assortment": True,
            }
        )
        action["context"] = ctx
        return action
