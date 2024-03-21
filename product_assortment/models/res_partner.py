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
        copy=False,
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
        domain_dic = {a: a._get_eval_partner_domain() for a in assortments}
        for partner in self:
            partner.applied_assortment_ids = assortments.filtered(
                lambda a: partner in a.partner_ids
                or domain_dic[a]
                and partner.filtered_domain(domain_dic[a])
            )

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        partners._update_partner_assortments()
        return partners

    def write(self, vals):
        res = super().write(vals)
        IrFilters = self.env["ir.filters"]
        if IrFilters.get_partner_domain_fields() & set(vals.keys()):
            self._update_partner_assortments()
        return res
