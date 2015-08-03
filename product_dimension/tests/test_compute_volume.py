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
        self.assertAlmostEqual(
            0.2,
            self.Product.onchange_calculate_volume(
                10., 200., 100., self.uom_cm.id
            )['value']['volume']
        )

    def test_it_computes_volume_in_meters(self):

        self.assertAlmostEqual(
            120.,
            self.Product.onchange_calculate_volume(
                6., 2., 10., self.uom_m.id
            )['value']['volume']
        )

    def setUp(self):
        super(TestComputeVolume, self).setUp()

        self.Product = self.env['product.product']
        self.uom_m = self.env['product.uom'].search([('name', '=', 'm')])
        self.uom_cm = self.env['product.uom'].search([('name', '=', 'cm')])
