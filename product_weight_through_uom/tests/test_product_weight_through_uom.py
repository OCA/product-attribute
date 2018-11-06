# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestWeightThroughUom(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestWeightThroughUom, cls).setUpClass()
        cls.kgm = cls.env.ref('product.product_uom_kgm')
        cls.ton = cls.env['product.uom'].create({
            'name': 'Test TON',
            'category_id': cls.kgm.category_id.id,
            'uom_type': 'bigger',
            'factor_inv': 1000,
        })
        cls.product1 = cls.env['product.product'].create({
            'name': 'test product 1',
            'type': 'product',
            'uom_id': cls.kgm.id,
            'uom_po_id': cls.kgm.id,
        })

    def test_01_uom_change(self):
        self.product1.uom_id = self.ton
        self.assertAlmostEqual(self.product1.weight, 1000)

    def test_02_extra_weight(self):
        self.product1.extra_weight = 0.33
        self.assertAlmostEqual(self.product1.weight, 1.33)
        self.product1.uom_id = self.ton
        self.assertAlmostEqual(self.product1.weight, 1000.33)
