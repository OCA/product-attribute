# Copyright 2015 OdooMRP team
# Copyright 2015 AvanzOSC
# Copyright 2015 Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def default_get(self, fields):
        res = super(ResPartner, self).default_get(fields)
        select_type = self.env.context.get("select_type", False)
        if select_type:
            res.update(
                {
                    "customer": select_type == "customer",
                    "supplier": select_type == "supplier",
                }
            )
        return res

    def action_view_customerinfo(self):
        self.ensure_one()
        customerinfo = self.env["product.customerinfo"].search(
            [("name", "child_of", self.commercial_partner_id.id)]
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": "product.customerinfo",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [("id", "in", customerinfo.ids)],
            "context": dict(
                self._context, default_name=self.id, visible_product_tmpl_id=False
            ),
            "name": _("Prices of customer"),
        }
