from openerp.tests import common


class TestVolumetricWeight(common.TransactionCase):

    def setUp(self):
        super(TestVolumetricWeight, self).setUp()

        self.product = self.env['product.product'].new()
        self.uom_m = self.env['product.uom'].search([('name', '=', 'm')])
        self.uom_m.write({'weight_volumetric_ratio': 400})
        self.uom_cm = self.env['product.uom'].search([('name', '=', 'cm')])
        self.uom_cm.write({'weight_volumetric_ratio': 400})

    def test_volumetric_weight_in_m(self):
        self.product.length = 1
        self.product.height = 1
        self.product.width = 1
        self.product.dimensional_uom_id = self.uom_m
        self.product.onchange_calculate_volume()
        self.assertAlmostEqual(
            400,
            self.product.weight_volumetric)

    def test_volumetric_weight_in_cm(self):
        self.product.length = 40
        self.product.height = 50
        self.product.width = 60
        self.product.dimensional_uom_id = self.uom_cm
        self.product.onchange_calculate_volume()
        self.assertAlmostEqual(
            48,
            self.product.weight_volumetric)
