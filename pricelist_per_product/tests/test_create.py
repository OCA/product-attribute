# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.tests.common import TransactionCase


class CreatePriceItemCase(TransactionCase):
    def test_create_from_product(self):
        """ Check if price item created from product template has:
            - price_discount = -1
            - base = 1
        """
        versions = self.env['product.pricelist.version'].search(
            [('pricelist_id.price_grid', '=', True)])
        version_values = {
            'price_version_id': versions[0].id, 'price_surcharge': 7}
        vals = {'name': 'Test from pricelist per product',
                'type': 'consu',
                'list_price': 10,
                'pricelist_item_ids': [(0, 0, version_values)]}
        product = self.env['product.template'].create(vals)
        item = self.env['product.pricelist.item'].search([
            ('product_tmpl_id', '=', product.id)])
        self.assertEqual(item.price_discount, -1.0)
        self.assertEqual(item.base, 1)
        self.assertEqual(versions[0].tmpl_in_count, 2)
