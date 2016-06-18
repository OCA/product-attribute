# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestProductPrefix(TransactionCase):

    def test_create_template(self):
        """Check that a prefix have been generated automatically.
        """
        tmpl = self.env['product.template'].create({'name': 'my template'})
        self.assertIsNotNone(tmpl.prefix_code)
        self.assertIsNot(tmpl.prefix_code, '/')

    def test_write_template(self):
        """Check that a prefix have been generated automatically.
        """
        tmpl = self.env['product.template'].create({'name': 'my template'})
        tmpl.write({'prefix_code': '/'})
        self.assertIsNotNone(tmpl.prefix_code)
        self.assertIsNot(tmpl.prefix_code, '/')
