# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV (<http://acsone.eu>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import openerp.tests.common as common
import psycopg2


class TestProductBrandSequence(common.TransactionCase):

    def _check_code(self, code):
        return code not in (False, '/')

    def test_sequence_on_product_brand(self):
        product_brand = self.env['product.brand']
        initial_pc = pc = product_brand.create({'name': 'cat1'})
        self.assertTrue(
            self._check_code(pc.code),
            "A brand has always a code.")
        pc.write({'code': 'my_code'})
        self.assertEquals(
            pc.code, 'my_code', "It must be possible to specify its own code.")
        pc = product_brand.create({'name': 'cat2',
                                   'code': 'my_code2'})
        self.assertEquals(
            pc.code, 'my_code2',
            "It must be possible to specify its own code.")
        pc.write({'code': False})
        self.assertTrue(
            self._check_code(pc.code),
            "A brand has always a code even if you try to reset the value "
            "on update.")

        with self.assertRaises(psycopg2.IntegrityError), \
                self.cr.savepoint():
            # check unique code
            product_brand.create({'name': 'cat3',
                                  'code': initial_pc.code})

        copy = pc.copy()
        self.assertTrue(
            self._check_code(copy.code),
            "A brand has always a code.")

        copy = pc.copy(default={'code': 'my_code3'})
        self.assertEquals(
            copy.code, 'my_code3',
            "It must be possible to specify its own code on copy.")
