#    Author: Leonardo Pistone
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
