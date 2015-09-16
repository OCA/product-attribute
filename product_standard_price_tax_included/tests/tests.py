# -*- coding: utf-8 -*-
##############################################################################
#
#    Product - Cost Price Tax Included Module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
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
#
##############################################################################

from openerp.tests.common import TransactionCase


class TestProductStandardPriceTaxIncluded(TransactionCase):
    """Tests for 'Cost Price Tax Included' Module"""

    def setUp(self):
        super(TestProductStandardPriceTaxIncluded, self).setUp()

        self.order_obj = self.env['sale.order']
        self.order_line_obj = self.env['sale.order.line']

        self.partner_id = self.ref(
            'product_standard_price_tax_included.partner_with_pricelist')
        self.product_id = self.ref(
            'product_standard_price_tax_included.product_product')
        self.pricelist_id = self.ref(
            'product_standard_price_tax_included.pricelist_price_tax_included')

    # Test Section
    def test_01_correct_tax_compute(self):
        """Test if the total of a sale order is correct with price
        based on Price List Tax Included."""

        # Create an Order
        order = self.order_obj.create({
            'partner_id': self.partner_id,
            'partner_invoice_id': self.partner_id,
            'partner_shipping_id': self.partner_id,
            'pricelist_id': self.pricelist_id,
        })

        # Create an Order line with a product with Tax Included
        res = self.order_line_obj.product_id_change(
            self.pricelist_id, self.product_id, qty=1,
            partner_id=self.partner_id)
        self.order_line_obj.create({
            'name': 'Sale Order Line Name',
            'order_id': order.id,
            'product_id': self.product_id,
            'tax_id': res['value']['tax_id'],
            'product_uom_qty': 1,
            'price_unit': res['value']['price_unit'],
        })

        order = self.order_obj.browse(order.id)
        self.assertEquals(
            order.amount_total, 11.5,
            "Computation of Price based on Cost Price Tax Included incorrect.")
