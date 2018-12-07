# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.fields import first
from odoo.osv import expression


class ProductCountryRestriction(models.Model):

    _name = 'product.country.restriction'
    _inherit = ['mail.thread']
    _description = 'Product Country Restriction'
    _order = 'sequence asc, id desc'

    name = fields.Char(
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        default=True,
        copy=False,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self._default_company_id(),
    )
    sequence = fields.Integer(
        default=10,
    )
    item_ids = fields.One2many(
        comodel_name='product.country.restriction.item',
        inverse_name='restriction_id',
        string='Country Restriction Items',
    )
    country_group_ids = fields.Many2many(
        relation='product_country_restriction_country_group_rel',
        comodel_name='res.country.group',
        column1='restriction_id',
        column2='group_id',
        string='Country Groups',
        help="Fill in this if you want that retriction apply on these groups"
             "(in addition to particular countries)."
    )
    country_ids = fields.Many2many(
        relation='product_country_restriction_country_rel',
        comodel_name='res.country',
        column1='restriction_id',
        column2='country_id',
        string='Countries',
        help="Fill in this if you want that restriction apply on these"
             "(in addition to country groups)."
    )
    resulting_country_ids = fields.Many2many(
        comodel_name='res.country',
        compute='_compute_resulting_country_ids',
        readonly=True,
    )

    @api.model
    def _default_company_id(self):
        return self.env['res.company']._company_default_get()

    @api.multi
    @api.depends('country_group_ids.country_ids', 'country_ids')
    def _compute_resulting_country_ids(self):
        for restriction in self:
            restriction.resulting_country_ids = \
                restriction.country_group_ids.mapped('country_ids') | \
                restriction.country_ids

    @api.model
    def _get_country_restriction_domain(self, countries, restriction_id=False):
        """
        Get Retrictions at once for all products
        :param countries:
        :param restriction_id: the restriction if knonwn. The search will
        return void recordset if countries can't apply
        :return:
        """
        country_domain = expression.OR([
            [('country_ids', 'in', countries.ids)],
            [('country_group_ids.country_ids', 'in', countries.ids)],
        ])
        if restriction_id:
            return expression.AND([
                [('id', '=', restriction_id.id)],
                country_domain,
            ])
        return country_domain

    @api.multi
    def _get_country_restriction_items_by_date(self, date):
        items = self.item_ids.filtered(
            lambda i: (not i.start_date or i.start_date <= date) and
            (not i.end_date or i.end_date >= date))
        return items

    def _update_result(self, applied_items, country, result):
        """
        Update result with the computed items
        :param result:
        :param product:
        :param country:
        :return:
        """
        if applied_items:
            for product, item in applied_items.iteritems():
                existing_items = result.get(product, [])
                existing_items.append((country, item))
                result.update({
                    product: existing_items,
                })
        return result

    @api.model
    def _get_restriction(
            self,
            product_by_country,
            date=False,
            restriction_id=False):
        """
        We return a dict with product as key and a list of tuples as
        value that correspond to asked countries and restriction item applied.
        There is only one item per product and per country
        :param product_by_partner: dict {country: product}
        :param date:
        :param restriction_id: restriction to apply if known (recordset)
        :return: dict {product: (countries, emabargo_item)}
        """
        if not date:
            date = fields.Date.today()
        res = {}
        countries = self.env['res.country'].browse()
        for country, product in product_by_country.iteritems():
            countries |= country

            domain = self._get_country_restriction_domain(
                countries,
                restriction_id,
            )
            restrictions = self.search(domain)

        for country, products in product_by_country.iteritems():
            restriction = first(restrictions.filtered(
                lambda r, c=country: c.id in r.country_ids.ids or
                c.id in r.country_group_ids.mapped('country_ids').ids))
            items = restriction._get_country_restriction_items_by_date(date)
            applied_items = items._get_country_restriction_item_by_rule(
                products)

            self._update_result(applied_items, country, res)

        return res

    @api.model
    def _get_country_restriction_messages(self, restrictions_by_product):
        """
        Parse the applied embargo items per product and generate the
        message
        :param: {product_id: [(country, item)]}
        :return:
        """
        res = ''
        messages = []
        for product, restrictions in restrictions_by_product.iteritems():
            for restriction in restrictions:
                messages.append(
                    _('The product %s has country restriction for %s.'
                      '(Rule : %s)') %
                    (product.name,
                     restriction[0].name,
                     restriction[1].name))
        res = '\n'.join(messages)
        return res
