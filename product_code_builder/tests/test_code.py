# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductCode(TransactionCase):
    """
        produit avec prefix interne PAS auto sans varainte: prefix dans prd.prd
        produit avec prefix interne auto sans varainte: prefix dans prd.prd
        produit avec prefix interne auto avec varainte: ordre des variantes
    """
    def test_automatic_code(self):
        """check codes are generated automatically
           with prefix and attribute order """
        retinas = [x.default_code
                   for x in self.prd_m.search(
                       [('product_tmpl_id', '=', self.retina_tmpl.id)])]
        retinas.sort()
        theoritical_retinas = ['RETW2.4CbM16', 'RETW2.4CwM16', 'RETW2.4CwM32']
        theoritical_retinas.sort()
        self.assertEqual(retinas, theoritical_retinas)

    def test_no_automatic_code(self):
        """ Check product code is not override by tmpl code """
        self.hard_disc_prd.write({'prefix_code': 'second'})
        # 'auto_default_code' is False on this product
        self.assertEqual(self.hard_disc_prd.prefix_code,
                         self.hard_disc_prd.default_code)
        self.hard_disc_prd.write({'prefix_code': 'last'})
        self.assertNotEqual(self.hard_disc_prd.prefix_code,
                            self.hard_disc_prd.default_code)

    def setUp(self):
        super(TestProductCode, self).setUp()
        self.prd_m = self.env['product.product']
        # product 'HDD SH-2' in demo data
        self.hard_disc_prd = self.env.ref('product.product_product_18')
        self.retina_tmpl = self.env.ref(
            'product.product_product_4_product_template')
