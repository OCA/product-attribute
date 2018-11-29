# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResCountry(models.Model):

    _inherit = 'res.country'

    product_country_restriction_ids = fields.Many2many(
        comodel_name='product.country.restriction',
        compute='_compute_product_country_restriction_ids',
    )
    product_country_restriction_count = fields.Integer(
        compute='_compute_product_country_restriction_count',
        readonly=True,)

    @api.depends('product_country_restriction_ids')
    def _compute_product_country_restriction_count(self):
        for country in self:
            country.product_country_restriction_count = \
                len(country.product_country_restriction_ids)

    @api.multi
    def _get_country_restriction_domain(self):
        return [
            '|',
            ('country_ids', 'in', self.ids),
            ('country_group_ids.country_ids', 'in', self.ids),
        ]

    @api.multi
    def _compute_product_country_restriction_ids(self):
        domain = self._get_country_restriction_domain()
        restrictions = self.env['product.country.restriction'].search(domain)
        for country in self:
            restrictions = restrictions.filtered(
                lambda r, c=country: c in r.country_ids or
                c in r.country_group_ids.mapped('country_ids'))
            country.product_country_restriction_ids = restrictions

    @api.multi
    def action_view_country_restrictions(self):
        self.ensure_one()
        ref = 'product_country_restriction.' \
              'product_country_restrictionact_window'
        country_id = self.id
        action_dict = self.env.ref(ref).read()[0]
        action_dict['domain'] = [
            '|',
            ('country_group_ids.country_ids', 'in', [country_id]),
            ('country_ids', 'in', [country_id])]
        return action_dict
