# Copyright 2018 ACSONE SA/NV
# Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


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

    state_id_domain = fields.Binary(
        compute="_compute_state_id_domain",
        help="Technical field, used to compute dynamically state domain"
        " depending on the country.",
    )

    @api.onchange("country_id")
    def onchange_country_id(self):
        if self.state_id and self.state_id.country_id != self.country_id:
            self.state_id = False

    @api.onchange("state_id")
    def onchange_state_id(self):
        if self.state_id:
            self.country_id = self.state_id.country_id

    @api.constrains("country_id", "state_id")
    def _check_country_id_state_id(self):
        for template in self.filtered(lambda x: x.state_id and x.country_id):
            if template.country_id != template.state_id.country_id:
                raise ValidationError(
                    _(
                        "The state '%(state_name)s' doesn't belong to"
                        " the country '%(country_name)s'",
                        state_name=template.state_id.name,
                        country_name=template.country_id.name,
                    )
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

    @api.depends("country_id")
    def _compute_state_id_domain(self):
        for template in self.filtered(lambda x: x.country_id):
            template.state_id_domain = [("country_id", "=", template.country_id.id)]
        for template in self.filtered(lambda x: not x.country_id):
            template.state_id_domain = []

    def _inverse_state_id(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.country_id = template.country_id

    def _get_related_fields_variant_template(self):
        res = super()._get_related_fields_variant_template()
        res += ["country_id", "state_id"]
        return res
