# coding: utf-8
# © 2017 Pierrick Brun <pierrick.brun@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo.tests.common import TransactionCase


class TestProductProduct(TransactionCase):
    def test_fields_view_get(self):
        product = self.help_create_product()
        product = product.with_context({'search_disable_custom_filters': True})
        root = etree.fromstring(product.fields_view_get()['arch'])
        for button in root.findall(".//button"):
            self.assertEquals('0', button.get('invisible'))

    def test_button_activate(self):
        self.help_button_active(False)

    def test_button_deactivate(self):
        self.help_button_active(True)

    def help_button_active(self, active=True):
        product = self.help_create_product(active)
        if active:
            product.button_deactivate()
        else:
            product.button_activate()
        self.assertEqual(product.active, not(active))

    def help_create_product(self, active=True):
        product = self.env['product.product'].create({
            'active': active,
            'name': 'test_product'
        })
        return product
