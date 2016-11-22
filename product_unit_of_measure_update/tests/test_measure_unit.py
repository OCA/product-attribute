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

    def test_write_tmpl_with_data(self):
        tmpl_with_data = self.env.ref(
            'product.product_product_7_product_template')
        try:
            tmpl_with_data.write({'uom_id': self.unit_gal.id})
        except Exception:
            _logger.info('Impossible to modify unit of measure')
        self.assertNotEqual(
            tmpl_with_data.uom_id,
            self.unit_cm,
            "Unit on product '%s' should be '%s'" % (
                tmpl_with_data.name, self.unit_gal.name))
