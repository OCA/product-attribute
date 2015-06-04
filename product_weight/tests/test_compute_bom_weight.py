#    Author: Florian da Costa
#    Copyright 2015 Akretion
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


class TestBomWeightCompute(TransactionCase):

    def test_calculate_bom_weight(self):
        self.component_1.weight_net = 0.15
        self.component_1.weight = 0.20
        self.component_2.weight_net = 0.18
        self.component_2.weight = 0.22
        self.component_3.weight_net = 0.64
        self.component_3.weight = 0.68
        self.env['product.weight.update'].calculate_product_bom_weight(
            self.bom)
        self.assertEqual(self.bom.product_tmpl_id.weight_net, 0.97)
        self.assertEqual(self.bom.product_tmpl_id.weight, 1.1)

    def setUp(self):
        super(TestBomWeightCompute, self).setUp()
        self.bom = self.env.ref('mrp.mrp_bom_11')
        self.component_1 = self.env.ref(
            'product.product_product_14_product_template')
        self.component_2 = self.env.ref(
            'product.product_product_15_product_template')
        self.component_3 = self.env.ref(
            'product.product_product_23_product_template')
