# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductProfile(TransactionCase):
    def test_check_hard_disc_product(self):
        # check route_ids
        real_routes = [x.id for x in self.hard_disc_prd.route_ids]
        theoritical_routes = [
            self.env.ref('mrp.route_warehouse0_manufacture').id,
            self.env.ref('stock.route_warehouse0_mto').id,
        ]
        real_routes.sort()
        theoritical_routes.sort()
        self.assertEqual(real_routes, theoritical_routes)
        # check categ_id
        theoritical_categ_id = self.env.ref('product.product_category_8')
        self.assertEqual(self.hard_disc_prd.categ_id.id,
                         theoritical_categ_id.id)

    def test_create_product(self):
        name = 'only name is specified'
        vals = {'profile_id': self.my_own_profile.id,
                'name': name}
        new_product = self.prd_m.create(vals)
        new_product._onchange_from_profile()
        count_prd = self.prd_m.search([('name', '=', name)])
        self.assertEqual(len(count_prd), 1)

    def test_write_template(self):
        vals = {'profile_id': self.my_own_profile.id}
        self.analysis_tmpl.write(vals)
        self.assertEqual(self.analysis_tmpl.profile_id, self.my_own_profile)

    def test_write_product(self):
        vals = {'profile_id': self.my_own_profile.id}
        self.analysis_prd.write(vals)
        self.assertEqual(self.analysis_prd.profile_id, self.my_own_profile)

    def test_product_tmpl_fields_view_get(self):
        view_id = self.env.ref('product.product_template_search_view').id
        res = self.hard_disc_prd.fields_view_get(
            view_id=view_id, view_type='search')
        self.assertTrue('string="My Own Type Saleable"' in res['arch'],
                        'string="My Own Type Saleable" must be in '
                        'fields_view_get() output')

    def setUp(self):
        super(TestProductProfile, self).setUp()
        self.prd_m = self.env['product.product']
        # product 'HDD SH-2' in demo data
        self.hard_disc_prd = self.env.ref('product.product_product_18')
        self.my_own_profile = self.env.ref('product_profile_example.own')
        self.analysis_tmpl = self.env.ref(
            'point_of_sale.partner_product_11_product_template')
        self.analysis_prd = self.env.ref(
            'point_of_sale.partner_product_11')
