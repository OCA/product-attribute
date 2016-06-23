# -*- coding: utf-8 -*-
# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestComputeVolume(TransactionCase):

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
        super(TestComputeVolume, self).setUp()

        self.product = self.env['product.product'].new()
        self.uom_m = self.env['product.uom'].search([('name', '=', 'm')])
        self.uom_cm = self.env['product.uom'].search([('name', '=', 'cm')])
