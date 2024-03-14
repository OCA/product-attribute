# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductStandardPriceTaxIncluded(TransactionCase):
    """Tests for 'Cost Price Tax Included' Module"""

    def setUp(self):
        super(TestProductStandardPriceTaxIncluded, self).setUp()

        self.SaleOrder = self.env["sale.order"]
        self.SaleOrderLine = self.env["sale.order.line"]

        self.partner = self.env.ref("base.res_partner_3")
        self.uom = self.env.ref("uom.product_uom_unit")
        self.product_tax_included = self.env.ref(
            "product_standard_price_tax_included.product_product_tax_included"
        )
        self.product_tax_excluded = self.env.ref(
            "product_standard_price_tax_included.product_product_tax_excluded"
        )
        self.pricelist_included = self.env.ref(
            "product_standard_price_tax_included.pricelist_price_tax_included"
        )
        self.pricelist_excluded = self.env.ref(
            "product_standard_price_tax_included.pricelist_price_tax_excluded"
        )

        # ensure that the currency of the price list is the same as
        # the main company to avoid error due to undesired conversion
        self.pricelist_included.currency_id = self.env.ref(
            "base.main_company"
        ).currency_id
        self.pricelist_excluded.currency_id = self.env.ref(
            "base.main_company"
        ).currency_id

        # Create an Order
        self.order = self.SaleOrder.create(
            {
                "partner_id": self.partner.id,
            }
        )

    # Test Section
    def test_01_test_standard_price_tax_included_product_vat_incl(self):
        self.assertEqual(self.product_tax_included.standard_price_tax_included, 1200)

    def test_02_test_standard_price_tax_included_product_vat_excl(self):
        self.assertEqual(self.product_tax_excluded.standard_price_tax_included, 120)

    def test_11_correct_tax_compute_tax_included(self):
        """Test if the total of a sale order is correct with pricelist
        based on standard price with tax included."""

        # Create an Order line with a product with Tax Included
        self.order.pricelist_id = self.pricelist_included
        self.SaleOrderLine.create(
            {
                "order_id": self.order.id,
                "product_id": self.product_tax_included.id,
                "product_uom_qty": 1,
                "product_uom": self.uom.id,
            }
        )
        # standard_price is 100 so standard_price vat incl is 120
        self.assertEqual(
            self.order.amount_total,
            1200.0,
            "Computation of Price based on Cost Price Tax Included incorrect.",
        )

    def test_12_correct_tax_compute_tax_included(self):
        """Test if the total of a sale order is correct with pricelist
        based on standard price with tax included.
        (No regression test)"""

        # Create an Order line with a product with Tax Excluded
        self.order.pricelist_id = self.pricelist_excluded
        self.SaleOrderLine.create(
            {
                "order_id": self.order.id,
                "product_id": self.product_tax_excluded.id,
                "product_uom_qty": 1,
                "product_uom": self.uom.id,
            }
        )
        # standard_price is 100 so standard_price vat incl is 120
        self.assertEqual(
            self.order.amount_total,
            120.0,
            "Computation of Price based on Cost Price incorrect. Regression.",
        )
