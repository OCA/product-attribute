# Copyright 2021 Tecnativa - Carlos Roca
# Copyright 2021 Tecnativa - Carlos Dauden
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    applied_assortment_ids = fields.Many2many(
        comodel_name="ir.filters",
        relation="ir_filter_all_partner_rel",
        column1="partner_id",
        column2="filter_id",
    )

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

    def _update_partner_assortments(self):
        # Using sudo to contemplate evaluation of domains with restricted fields
        self = self.sudo()
        assortments = self.env["ir.filters"].search([("is_assortment", "=", True)])
        for partner in self:
            # Use ids instead of record to improve performance (Remove in next versions)
            partner_assortment_ids = []
            for assortment in assortments:
                if partner in assortment.partner_ids or partner.filtered_domain(
                    assortment._get_eval_partner_domain()
                ):
                    partner_assortment_ids.append(assortment.id)
            partner.applied_assortment_ids = assortments.browse(partner_assortment_ids)

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        self._update_partner_assortments()
        return partners

    def write(self, vals):
        res = super().write(vals)
        IrFilters = self.env["ir.filters"]
        if IrFilters.get_partner_domain_fields() & set(vals.keys()):
            self._update_partner_assortments()
        return res
