# -*- coding: utf-8 -*-
# Copyright 2019 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleReport(models.Model):
    _inherit = 'sale.report'

    list_categories = fields.Char(
        string='List Categories',
        readonly=True)

    def _select(self):
        res = super(SaleReport, self)._select()
        return res + ', \';\' || array_to_string(array_agg(' \
            'DISTINCT list_categ.categ_id), \';\', \'-\') || \';\' '\
            'AS list_categories'

    def _from(self):
        res = super(SaleReport, self)._from()
        return res + ' LEFT JOIN product_list_categ_rel list_categ ON (' \
                     'list_categ.product_id = t.id)'

    def get_list_categories_domain(self, input_domain):
        category_obj = self.env['product.category']

        operator = input_domain[1]
        value = input_domain[2]
        res_domain = []

        if operator == '!=' and not value:
            # It is set:
            res_domain.append(('list_categories', '!=', ';-;'))
            return res_domain
        elif operator == '=' and not value:
            # It's not set:
            res_domain.append(('list_categories', '=', ';-;'))
            return res_domain

        if operator in ('not ilike', 'not like'):
            neg_operator = operator[4:]
            categories = category_obj.search([('name', neg_operator, value)])
        else:
            categories = category_obj.search([('name', operator, value)])
        if categories:
            i = 0
            if operator == '=':
                operator = 'like'
            elif operator == '!=':
                operator = 'not like'
            for categ in categories:
                if i+1 < len(categories) and operator in ('like', 'ilike'):
                    res_domain.append('|')
                categ_str = ';' + str(categ.id) + ';'
                domain_tuple = ('list_categories', operator, categ_str)
                res_domain.append(domain_tuple)
                i += 1
        else:
            # category does not exists,
            # so search for an inexistent list_categories:
            domain_tuple = ('list_categories', operator, ';;;')
            res_domain.append(domain_tuple)

        return res_domain

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None,
                   orderby=False, lazy=True):
        new_domain = []
        for domain_tuple in domain:
            if domain_tuple[0] == 'list_categories':
                new_domain += self.get_list_categories_domain(domain_tuple)
            else:
                new_domain.append(domain_tuple)

        result = super(SaleReport, self).read_group(
            new_domain, fields, groupby, offset=offset, limit=limit,
            orderby=orderby, lazy=lazy)

        return result
