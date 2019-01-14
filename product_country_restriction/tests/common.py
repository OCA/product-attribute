# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common


class CountryRestrictionCommon(common.TransactionCase):

    def setUp(self):
        super(CountryRestrictionCommon, self).setUp()
        self.restriction_obj = self.env['product.country.restriction']
        self.rule_obj = self.env['product.country.restriction.rule']
        self.product_1 = self.env.ref('product.product_product_1')
        self.product_2 = self.env.ref('product.product_product_2')
        self.product_3 = self.env.ref(
            'product.product_product_3').product_tmpl_id
        self.product_4 = self.env.ref('product.product_product_4')
        # Product with no rule
        self.product_5 = self.env.ref('product.product_product_5')
        self.partner = self.env.ref('base.res_partner_2')
        self.au = self.env.ref('base.au')
        self.kp = self.env.ref('base.kp')
        self.be = self.env.ref('base.be')

        vals = {
            'parent_id': self.env.ref('product.product_category_all').id,
            'name': 'Category Limited',
        }
        self.categ = self.env['product.category'].create(vals)

        self.product_4.write({
            'categ_id': self.categ.id,
        })

        vals = {
            'name': 'Australia & Philippines',
            'country_ids': [(6, 0, [
                self.env.ref('base.au').id,
                self.env.ref('base.ph').id,
            ])]
        }
        self.country_group = self.env['res.country.group'].create(vals)

        vals = {
            'name': 'Australia & Philippines Restriction',
            'company_id': self.env.user.company_id.id,
            'country_group_ids': [(6, 0, [self.country_group.id])],
        }

        self.restriction_1 = self.restriction_obj.create(vals)

        vals = {
            'restriction_id': self.restriction_1.id,
            'rule_id': self.rule_obj._get_by_code('global').id,
        }
        self.global_item = self.env[
            'product.country.restriction.item'].create(vals)

        vals = {
            'name': 'North Korea',
            'company_id': self.env.user.company_id.id,
            'country_ids': [(6, 0, [self.kp.id])],
        }

        self.restriction_2 = self.restriction_obj.create(vals)

        vals = {
            'restriction_id': self.restriction_2.id,
            'rule_id': self.rule_obj._get_by_code('variant').id,
            'product_id': self.product_2.id,
            'start_date': '2018-03-01',
            'end_date': '2018-04-30',
        }
        self.variant_item = self.env[
            'product.country.restriction.item'].create(vals)

        vals = {
            'restriction_id': self.restriction_2.id,
            'rule_id': self.rule_obj._get_by_code('product').id,
            'product_template_id': self.product_3.id,
            'start_date': '2018-06-01',
            'end_date': '2018-12-31',
        }
        self.product_item = self.env[
            'product.country.restriction.item'].create(vals)

        vals = {
            'restriction_id': self.restriction_2.id,
            'rule_id': self.rule_obj._get_by_code('category').id,
            'product_category_id': self.categ.id,
            'start_date': '2018-06-01',
        }
        self.category_item = self.env[
            'product.country.restriction.item'].create(vals)
