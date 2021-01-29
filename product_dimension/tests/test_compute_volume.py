# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestComputeVolumeOnProduct(TransactionCase):

    def test_it_computes_volume_in_cm(self):
        self.product.product_length = 10.
        self.product.product_height = 200.
        self.product.product_width = 100.
        self.product.dimensional_uom_id = self.uom_cm
        self.product.volume_uom_id = self.uom_litre
        self.product.onchange_calculate_volume()
        self.assertAlmostEqual(
            200,
            self.product.volume
        )

    def test_it_computes_volume_in_meters(self):
        self.product.product_length = 6.
        self.product.product_height = 2.
        self.product.product_width = 10.
        self.product.dimensional_uom_id = self.uom_m
        self.product.volume_uom_id = self.uom_litre
        self.product.onchange_calculate_volume()
        self.assertAlmostEqual(
            120000,
            self.product.volume
        )

    def setUp(self):
        super(TestComputeVolumeOnProduct, self).setUp()

        self.product = self.env['product.product'].new()
        self.uom_m = self.env['uom.uom'].search([('name', '=', 'm')])
        self.uom_cm = self.env['uom.uom'].search([('name', '=', 'cm')])
        self.uom_litre = self.env.ref("uom.product_uom_litre")


class TestComputeVolumeOnTemplate(TransactionCase):

    def test_it_computes_volume_in_cm(self):
        self.template.product_length = 10.
        self.template.product_height = 200.
        self.template.product_width = 100.
        self.template.dimensional_uom_id = self.uom_cm
        self.template.volume_uom_id = self.uom_litre
        self.template.onchange_calculate_volume()
        self.assertAlmostEqual(
            200,
            self.template.volume
        )

    def test_it_computes_volume_in_meters(self):
        self.template.product_length = 6.
        self.template.product_height = 2.
        self.template.product_width = 10.
        self.template.dimensional_uom_id = self.uom_m
        self.template.volume_uom_id = self.uom_litre
        self.template.onchange_calculate_volume()
        self.assertAlmostEqual(
            120000,
            self.template.volume
        )

    def setUp(self):
        super(TestComputeVolumeOnTemplate, self).setUp()

        self.template = self.env['product.template'].new()
        self.uom_m = self.env['uom.uom'].search([('name', '=', 'm')])
        self.uom_cm = self.env['uom.uom'].search([('name', '=', 'cm')])
        self.uom_litre = self.env.ref("uom.product_uom_litre")
