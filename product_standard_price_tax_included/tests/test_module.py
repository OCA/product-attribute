# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductStandardPriceTaxIncluded(TransactionCase):
    """Tests for 'Cost Price Tax Included' Module"""

    def setUp(self):
        super(TestProductStandardPriceTaxIncluded, self).setUp()

        self.SaleOrder = self.env['sale.order']
        self.SaleOrderLine = self.env['sale.order.line']

        self.tax = self.env.ref(
            'product_standard_price_tax_included.account_tax_tax_included')
        self.partner = self.env.ref('base.res_partner_3')
        self.uom = self.env.ref('uom.product_uom_unit')
        self.product = self.env.ref(
            'product_standard_price_tax_included.product_product')
        self.pricelist = self.env.ref(
            'product_standard_price_tax_included.pricelist_price_tax_included')

    # Test Section
    def test_01_correct_tax_compute(self):
        """Test if the total of a sale order is correct with price
        based on Price List Tax Included."""

        # Create an Order
        order = self.SaleOrder.create({
            'partner_id': self.partner.id,
            'pricelist_id': self.pricelist.id,
        })

        # Create an Order line with a product with Tax Included
        self.SaleOrderLine.create({
            'order_id': order.id,
            'product_id': self.product.id,
            'product_uom_qty': 1,
            'product_uom': self.uom.id,
        })
        self.assertEquals(
            order.amount_total, 12.0,
            "Computation of Price based on Cost Price Tax Included incorrect.")
