# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import Warning as UserError


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
        retina_tmpl = self.env.ref(
            'product.product_product_4_product_template')
        retina_tmpl.write({'auto_default_code': True})
        retinas = [x.default_code for x in retina_tmpl.product_variant_ids]
        retinas.sort()
        self.assertEqual(
            retinas, ['RETW2.4CbM16', 'RETW2.4CwM16', 'RETW2.4CwM32'])

    def test_change_sequence_attribute(self):
        """Check codes generated automatically.

        with prefix and attribute order
        """
        retina_tmpl = self.env.ref(
            'product.product_product_4_product_template')
        retina_tmpl.write({'auto_default_code': True})
        # Change the sequence of Color
        self.env.ref('product.product_attribute_2').write({'sequence': 2})
        retinas = [x.default_code for x in retina_tmpl.product_variant_ids]
        retinas.sort()
        self.assertEqual(
            retinas, ['RETCbW2.4M16', 'RETCwW2.4M16', 'RETCwW2.4M32'])

    def test_modify_automatic_code(self):
        with self.assertRaises(UserError):
            retina_tmpl = self.env.ref(
                'product.product_product_4_product_template')
            retina_tmpl.write({'auto_default_code': True})
            retina_tmpl.product_variant_ids[0].write({
                'default_code': 'stop me'})

    def test_allow_manual_default_code(self):
        """It should allow a user defined default code.

        When auto_default_code is false : default_code can be set by user
        Then, when auto_default_code is set to true, a default_code
        should be generated
        """

        # hard_disc_prd is set in with auto_default_code = false
        hard_disc_prd = self.env.ref('product.product_product_18')

        # ensure we can set a default code manually
        hard_disc_prd.write({'default_code': 'from_product'})
        self.assertEqual(hard_disc_prd.default_code, 'from_product')

        # ensure we can set the default code from the template
        hard_disc_prd.write({'default_code': 'from_template'})
        self.assertEqual(hard_disc_prd.default_code, 'from_template')

    def test_creating_product_with_default_code(self):
        product = self.env['product.product'].create({
            'name': 'Test',
            'default_code': 'product_default_code',
            })
        self.assertEqual(product.default_code, 'product_default_code')

    def test_creating_product_template_with_default_code(self):
        product = self.env['product.template'].create({
            'name': 'Test',
            'default_code': 'product_template_default_code',
            })
        self.assertEqual(product.default_code, 'product_template_default_code')
