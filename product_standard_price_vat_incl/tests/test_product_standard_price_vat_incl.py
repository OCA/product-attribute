# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Standard Price VAT Included Module for Odoo
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


class TestProductStandardPriceVATIncluded(TransactionCase):
    """Tests for 'Product Standard Price VAT Included' Module"""

    def setUp(self):
        super(TestProductStandardPriceVATIncluded, self).setUp()
        cr, uid = self.cr, self.uid

        self.imd_obj = self.registry('ir.model.data')
        self.so_obj = self.registry('sale.order')
        self.sol_obj = self.registry('sale.order.line')
        self.partner_id = self.imd_obj.get_object_reference(
            cr, uid, 'product_standard_price_vat_incl',
            'partner_with_pricelist')[1]
        self.pricelist_id = self.imd_obj.get_object_reference(
            cr, uid, 'product_standard_price_vat_incl',
            'pricelist_standard_price_vat_incl')[1]
        self.product_id = self.imd_obj.get_object_reference(
            cr, uid, 'product_standard_price_vat_incl',
            'product_product')[1]

    # Test Section
    def test_01_correct_vat_compute(self):
        """Test if the total of a sale order is correct with price
        based on Price List VAT Included."""
        cr, uid = self.cr, self.uid
        so_id = self.so_obj.create(cr, uid, {
            'partner_id': self.partner_id,
            'partner_invoice_id': self.partner_id,
            'partner_shipping_id': self.partner_id,
            'pricelist_id': self.pricelist_id,
        })

        res = self.sol_obj.product_id_change(
            cr, uid, [], self.pricelist_id, self.product_id, qty=1,
            partner_id=self.partner_id)
        self.sol_obj.create(cr, uid, {
            'name': 'Sale Order Line Name',
            'order_id': so_id,
            'product_id': self.product_id,
            'tax_id': res['value']['tax_id'],
            'product_uom_qty': 1,
            'price_unit': res['value']['price_unit'],
        })

        so = self.so_obj.browse(cr, uid, so_id)
        self.assertEquals(
            so.amount_total, 11.5,
            """Computation of Price based on Cost VAT Included incorrect.""")
