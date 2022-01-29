# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import datetime, safe_eval


class IrFilters(models.Model):
    _inherit = "ir.filters"

    @api.model
    def _get_default_is_assortment(self):
        if self.env.context.get("product_assortment", False):
            return True
        return False

    @api.model
    def _update_assortment_default_values(self, vals_list):
        """
        If we create the filter through the assortment, we need to force
        model_id to product.product
        """
        product_assortment = self.env.context.get("product_assortment", False)
        if not product_assortment:
            return vals_list
        model = self.env.ref("product.model_product_product")
        for vals in vals_list:
            if not vals.get("model_id"):
                vals.update({"model_id": model.model})
        return vals_list

    @api.model_create_multi
    def create(self, vals_list):
        self._update_assortment_default_values(vals_list=vals_list)
        return super().create(vals_list=vals_list)

    partner_ids = fields.Many2many(
        comodel_name="res.partner",
        help="This field allow to relate a partner to a domain of products",
        default=lambda p: p.env.context.get("default_partner_ids"),
    )

    blacklist_product_ids = fields.Many2many(
        comodel_name="product.product", relation="assortment_product_blacklisted"
    )

    whitelist_product_ids = fields.Many2many(
        comodel_name="product.product", relation="assortment_product_whitelisted"
    )

    record_count = fields.Integer(compute="_compute_record_count")

    is_assortment = fields.Boolean(default=lambda x: x._get_default_is_assortment())
    partner_domain = fields.Text(default="[]", required=True)
    all_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        compute="_compute_all_partner_ids",
    )

    @api.depends("partner_ids", "partner_domain")
    def _compute_all_partner_ids(self):
        """Summarize selected partners and partners from partner domain field"""
        for ir_filter in self:
            if not ir_filter.is_assortment:
                ir_filter.all_partner_ids = False
            elif ir_filter.partner_domain != "[]":
                ir_filter.all_partner_ids = (
                    self.env["res.partner"].search(ir_filter._get_eval_partner_domain())
                    + ir_filter.partner_ids
                )
            else:
                ir_filter.all_partner_ids = ir_filter.partner_ids

    def _get_eval_domain(self):
        res = super()._get_eval_domain()

        if self.whitelist_product_ids:
            result_domain = [("id", "in", self.whitelist_product_ids.ids)]
            res = expression.OR([result_domain, res])

        if self.blacklist_product_ids:
            result_domain = [("id", "not in", self.blacklist_product_ids.ids)]
            res = expression.AND([result_domain, res])

        return res

    def _get_eval_partner_domain(self):
        self.ensure_one()
        return safe_eval(
            self.partner_domain,
            {"datetime": datetime, "context_today": datetime.datetime.now},
        )

    def _compute_record_count(self):
        for record in self:
            if record.model_id not in self.env:
                # invalid model
                record.record_count = 0
                continue
            domain = record._get_eval_domain()
            record.record_count = self.env[record.model_id].search_count(domain)

    @api.model
    def _get_action_domain(self, action_id=None):
        # tricky way to act on get_filter method to prevent returning
        # assortment in search view filters
        domain = super()._get_action_domain(action_id=action_id)
        domain = expression.AND([[("is_assortment", "=", False)], domain])

        return domain

    def show_products(self):
        self.ensure_one()
        xmlid = "product.product_normal_action_sell"
        action = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
        action.update(
            {
                "domain": self._get_eval_domain(),
                "name": _("Products"),
                "context": self.env.context,
                "target": "current",
            }
        )
        return action
