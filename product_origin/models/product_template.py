# Copyright 2018 ACSONE SA/NV
# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    country_id = fields.Many2one(
        comodel_name="res.country",
        compute="_compute_country_id",
        inverse="_inverse_country_id",
        string="Country of Origin",
        store=True,
    )

    state_id = fields.Many2one(
        comodel_name="res.country.state",
        compute="_compute_state_id",
        inverse="_inverse_state_id",
        string="Country State of Origin",
        store=True,
    )

    @api.depends("product_variant_ids", "product_variant_ids.country_id")
    def _compute_country_id(self):
        for template in self:
            if template.product_variant_count == 1:
                template.country_id = template.product_variant_ids.country_id
            else:
                template.country_id = False

    def _inverse_country_id(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.country_id = template.country_id

    @api.depends("product_variant_ids", "product_variant_ids.state_id")
    def _compute_state_id(self):
        for template in self:
            if template.product_variant_count == 1:
                template.state_id = template.product_variant_ids.state_id
            else:
                template.state_id = False

    def _inverse_state_id(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.country_id = template.country_id

    def _get_related_fields_variant_template(self):
        res = super()._get_related_fields_variant_template()
        res += ["country_id", "state_id"]
        return res
