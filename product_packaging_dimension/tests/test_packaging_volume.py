# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestPackagingVolumeCompute(TransactionCase):
    def setUp(self):
        super(TestPackagingVolumeCompute, self).setUp()

        self.packaging = self.env["product.packaging"].new()
        self.packaging2 = self.env["product.packaging"].new()
        self.packaging3 = self.env["product.packaging"].new()

        self.uom_m = self.env["uom.uom"].search([("name", "=", "m")])
        self.uom_cm = self.env["uom.uom"].search([("name", "=", "cm")])
        self.uom_L = self.env["uom.uom"].search([("name", "=", "L")])
        self.uom_m3 = self.env["uom.uom"].search([("name", "=", "m³")])
        self.uom_ft = self.env["uom.uom"].search([("name", "=", "ft")])
        self.uom_ft3 = self.env["uom.uom"].search([("name", "=", "ft³")])

    def test_input_uom(self):
        # Volume always in m3 (using default parameter), but with different initial UoM.

        # Initial dimensions in meter
        self.packaging.packaging_length = 10.0
        self.packaging.height = 10.0
        self.packaging.width = 10.0
        self.packaging.length_uom_id = self.uom_m
        self.packaging.volume_uom_id = self.uom_m3
        self.packaging._compute_volume()
        self.assertEqual(1000, self.packaging.volume)

        #  Initial dimensions in cm
        self.packaging2.packaging_length = 10.0
        self.packaging2.height = 10.0
        self.packaging2.width = 10.0
        self.packaging2.length_uom_id = self.uom_cm
        self.packaging2.volume_uom_id = self.uom_m3
        self.packaging2._compute_volume()
        self.assertEqual(0.001, self.packaging2.volume)

        # Initial dimensions in feet
        self.packaging3.packaging_length = 10.0
        self.packaging3.height = 10.0
        self.packaging3.width = 10.0
        self.packaging3.length_uom_id = self.uom_ft
        self.packaging3.volume_uom_id = self.uom_m3
        self.packaging3._compute_volume()
        self.assertEqual(28.3168, self.packaging3.volume)

    def test_compute_volume(self):
        # initial UoM always in meters and Volume in m3, but with different dimensions.

        self.packaging.packaging_length = 10
        self.packaging.height = 8
        self.packaging.width = 10
        self.packaging.length_uom_id = self.uom_m
        self.packaging.volume_uom_id = self.uom_m3
        self.packaging._compute_volume()
        self.assertEqual(800, self.packaging.volume)

        self.packaging2.packaging_length = 6.0
        self.packaging2.height = 14.0
        self.packaging2.width = 1.0
        self.packaging2.length_uom_id = self.uom_m
        self.packaging2.volume_uom_id = self.uom_m3
        self.packaging2._compute_volume()
        self.assertEqual(84.0, self.packaging2.volume)

        self.packaging3.packaging_length = 100.0
        self.packaging3.height = 50
        self.packaging3.width = 80
        self.packaging3.length_uom_id = self.uom_m
        self.packaging3.volume_uom_id = self.uom_m3
        self.packaging3._compute_volume()
        self.assertEqual(400000, self.packaging3.volume)

    def test_output_uom(self):
        # Tests with both different initial and volume UoMs.

        # feet to Liters
        self.packaging.packaging_length = 10.0
        self.packaging.height = 10.0
        self.packaging.width = 10.0
        self.packaging.length_uom_id = self.uom_ft
        self.packaging.volume_uom_id = self.uom_L
        self.packaging._compute_volume()
        self.assertAlmostEqual(28316.8439, self.packaging.volume)

        #  cm to cubic feet
        self.packaging2.packaging_length = 10.0
        self.packaging2.height = 10.0
        self.packaging2.width = 10.0
        self.packaging2.length_uom_id = self.uom_cm
        self.packaging2.volume_uom_id = self.uom_ft3
        self.packaging2._compute_volume()
        self.assertAlmostEqual(0.0353, self.packaging2.volume)

        # meters to cubic feet
        self.packaging3.packaging_length = 10.0
        self.packaging3.height = 10.0
        self.packaging3.width = 10.0
        self.packaging3.length_uom_id = self.uom_m
        self.packaging3.volume_uom_id = self.uom_ft3
        self.packaging3._compute_volume()
        self.assertAlmostEqual(35314.7248, self.packaging3.volume)
