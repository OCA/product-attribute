# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductCode(TransactionCase):
    """Test default_code.

    Generated automatically
    Manually entered
    Ensure order
    """

    def test_automatic_code(self):
        """Check codes generated automatically.

        with prefix and attribute order
        """
        retinas = [x.default_code
                   for x in self.prd_m.search(
                       [('product_tmpl_id', '=', self.retina_tmpl.id)])]
        retinas.sort()
        theoritical_retinas = ['RETW2.4CbM16', 'RETW2.4CwM16', 'RETW2.4CwM32']
        theoritical_retinas.sort()
        self.assertEqual(retinas, theoritical_retinas)

    def test_allow_manual_default_code(self):
        """It should allow a user defined default code.

        When auto_default_code is false : default_code can be set by user
        Then, when auto_default_code is set to true, a default_code
        should be generated
        """
        manual_default_code = 'user_entered'

        # hard_disc_prd is set in with auto_default_code = false

        # ensure we can set a default code manually
        self.hard_disc_prd.write({'default_code': manual_default_code})
        self.assertEqual(self.hard_disc_prd.default_code, manual_default_code)

        # trigger _comput_default_code, ensure code is still the same
        self.hard_disc_prd.write({'prefix_code': 'another_prefix'})
        self.assertEqual(self.hard_disc_prd.default_code, manual_default_code)

        # ensure this default code is lost when auto_default_code
        # is changed to true
        self.hard_disc_prd.write({'auto_default_code': True})
        self.assertNotEqual(
            self.hard_disc_prd.default_code,
            manual_default_code)

    def setUp(self):
        super(TestProductCode, self).setUp()
        self.prd_m = self.env['product.product']
        # product 'HDD SH-2' in demo data
        self.hard_disc_prd = self.env.ref('product.product_product_18')
        self.retina_tmpl = self.env.ref(
            'product.product_product_4_product_template')
