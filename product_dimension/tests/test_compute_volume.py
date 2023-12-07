# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestComputeVolumeOnProduct(TransactionCase):
    def test_it_computes_volume_in_cm(self):
        self.product.product_length = 10.0
        self.product.product_height = 200.0
        self.product.product_width = 100.0
        self.product.dimensional_uom_id = self.uom_cm
        self.assertAlmostEqual(0.2, self.product.volume)
        self.product.volume = 1.0
        self.assertAlmostEqual(1.0, self.product.volume)

    def test_it_computes_volume_in_meters(self):
        self.product.product_length = 6.0
        self.product.product_height = 2.0
        self.product.product_width = 10.0
        self.product.dimensional_uom_id = self.uom_m
        self.assertAlmostEqual(120, self.product.volume)

    def setUp(self):
        super().setUp()

        self.product = self.env["product.product"].new()
        self.uom_m = self.env["uom.uom"].search([("name", "=", "m")])
        self.uom_cm = self.env["uom.uom"].search([("name", "=", "cm")])


class TestComputeVolumeOnTemplate(TransactionCase):
    def test_it_computes_volume_in_cm(self):
        self.template.product_length = 10.0
        self.template.product_height = 200.0
        self.template.product_width = 100.0
        self.template.dimensional_uom_id = self.uom_cm
        self.assertAlmostEqual(0.2, self.template.volume)
        self.template.volume = 1.0
        self.assertAlmostEqual(1.0, self.template.volume)

    def test_it_computes_volume_in_meters(self):
        self.template.product_length = 6.0
        self.template.product_height = 2.0
        self.template.product_width = 10.0
        self.template.dimensional_uom_id = self.uom_m
        self.assertAlmostEqual(120, self.template.volume)

    def setUp(self):
        super().setUp()

        self.template = self.env["product.template"].new()
        self.uom_m = self.env["uom.uom"].search([("name", "=", "m")])
        self.uom_cm = self.env["uom.uom"].search([("name", "=", "cm")])
