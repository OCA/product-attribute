# coding: utf-8
# © 2016 David BEAL @ Akretion <david.beal@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
import logging

_logger = logging.getLogger(__name__)


class TestMeasureUnit(TransactionCase):

    def setUp(self):
        super(TestMeasureUnit, self).setUp()
        self.unit_cm = self.env.ref('product.product_uom_cm')
        self.unit_day = self.env.ref('product.product_uom_day')
        self.unit_gal = self.env.ref('product.product_uom_gal')

    def test_10_prod_tmpl_not_used(self):
        # Datacard product
        product = self.env.ref(
            'product.product_product_9_product_template')
        # write should NOT fails
        self.try2write_product(product, self.unit_gal, self.unit_day)
        self.assertEqual(
            product.uom_id,
            self.unit_gal,
            "Unit on product '%s' should be '%s'" % (
                product.name, self.unit_gal.name))
        self.assertEqual(
            product.uom_po_id,
            self.unit_day,
            "Unit on product '%s' should be '%s'" % (
                product.name, self.unit_day.name))

    def test_20_product_used(self):
        product = self.env.ref(
            'product.product_product_46')
        procurement_data = {
            'name': 'test',
            'product_id': product.id,
            'product_qty': 2,
            'product_uom': product.uom_id.id,
        }
        self.env['procurement.order'].create(procurement_data)
        # write should fails
        self.try2write_product(product, self.unit_gal, self.unit_day)
        self.assertNotEqual(
            product.uom_id,
            self.unit_gal,
            "Unit on product '%s' should NOT be '%s'" % (
                product.name, self.unit_gal.name))

    def try2write_product(self, product, uom, uom_po):
        try:
            # even if write fails
            # we need to go further in the test
            product.write({
                'uom_id': uom.id,
                'uom_po_id': uom_po.id,
            })
        except Exception:
            _logger.info('Impossible to update unit of measure')
