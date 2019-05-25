# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestComputeVolumeOnProduct(TransactionCase):

    def test_it_computes_volume_in_cm(self):
        self.product.length = 10.
        self.product.height = 200.
        self.product.width = 100.
        self.product.dimensional_uom_id = self.uom_cm
        self.product.onchange_calculate_volume()
        self.assertAlmostEqual(
            0.2,
            self.product.volume
        )

    def test_it_computes_volume_in_meters(self):
        self.product.length = 6.
        self.product.height = 2.
        self.product.width = 10.
        self.product.dimensional_uom_id = self.uom_m
        self.product.onchange_calculate_volume()
        self.assertAlmostEqual(
            120,
            self.product.volume
        )

    def setUp(self):
        super(TestComputeVolumeOnProduct, self).setUp()

        self.product = self.env['product.product'].new()
        self.uom_m = self.env['uom.uom'].search([('name', '=', 'm')])
        self.uom_cm = self.env['uom.uom'].search([('name', '=', 'cm')])


class TestComputeVolumeOnTemplate(TransactionCase):

    def test_it_computes_volume_in_cm(self):
        self.template.length = 10.
        self.template.height = 200.
        self.template.width = 100.
        self.template.dimensional_uom_id = self.uom_cm
        self.template.onchange_calculate_volume()
        self.assertAlmostEqual(
            0.2,
            self.template.volume
        )

    def test_it_computes_volume_in_meters(self):
        self.template.length = 6.
        self.template.height = 2.
        self.template.width = 10.
        self.template.dimensional_uom_id = self.uom_m
        self.template.onchange_calculate_volume()
        self.assertAlmostEqual(
            120,
            self.template.volume
        )

    def setUp(self):
        super(TestComputeVolumeOnTemplate, self).setUp()

        self.template = self.env['product.template'].new()
        self.uom_m = self.env['uom.uom'].search([('name', '=', 'm')])
        self.uom_cm = self.env['uom.uom'].search([('name', '=', 'cm')])
