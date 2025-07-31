# Copyright 2025 360ERP (<https://www.360erp.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.addons.base.tests.common import BaseCommon


class TestPurchasePrice(BaseCommon):
    def setUp(self):
        super().setUp()
        self.product = self.env["product.product"].create(
            {"name": "product_test", "standard_price": 1.0}
        )
        self.company_1 = self.env.company
        self.currency = self.env.ref("base.USD")
        self.other_currency = self.env.ref("base.EUR")
        self.other_currency.action_unarchive()
        other_companies = self.env["res.company"].search([]) - self.company_1
        other_companies.active = False
        self.env.flush_all()
        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "company_id": self.company_1.id,
            }
        )

    def _update_product_avg_prices(self):
        self.env.flush_all()
        self.env["product.template"].update_average_purchase_price(
            self.product.product_tmpl_id
        )

    def _setup_other_company(self):
        self.company_2 = self.env["res.company"].create(
            {
                "name": "company2",
                "currency_id": self.currency.id,
            }
        )

    def _create_po(self, price=0.0, confirm=True, company=False, currency=False):
        po = self.env["purchase.order"].create(
            {
                "partner_id": self.partner.id,
                "currency_id": self.env.ref("base.USD").id
                if not currency
                else currency.id,
            }
        )
        self.env["purchase.order.line"].create(
            {
                "order_id": po.id,
                "product_id": self.product.id,
                "product_qty": 1.0,
                "price_unit": price,
            }
        )
        if company:
            po.company_id = company
        if confirm:
            po.state = "purchase"
        return po

    def test_average_purchase_price(self):
        po = self._create_po(3.0, confirm=False)
        self._update_product_avg_prices()
        self.assertFalse(
            self.product.average_purchase_price,
            "Average purchase price should be 0.0 before confirming the purchase order",
        )
        po.state = "purchase"
        self._update_product_avg_prices()
        self.assertAlmostEqual(self.product.average_purchase_price, 3.0, places=2)
        self._create_po(7.0)
        self._update_product_avg_prices()
        self.assertAlmostEqual(self.product.average_purchase_price, 5.0, places=2)
        self._create_po(999.0, confirm=False)
        self._update_product_avg_prices()
        self.assertAlmostEqual(
            self.product.average_purchase_price,
            5.0,
            places=2,
            msg="Non confirmed POs should not affect the average purchase price",
        )

    def test_average_purchase_price_multicompany_shared(self):
        self._setup_other_company()
        self._create_po(4.0, company=self.company_1)
        self._update_product_avg_prices()
        tmpl = self.product.product_tmpl_id
        self.assertEqual(tmpl.with_company(self.company_1).average_purchase_price, 4.0)
        self.assertEqual(tmpl.with_company(self.company_2).average_purchase_price, 4.0)

    def test_average_purchase_price_multicompany_not_shared(self):
        self._setup_other_company()
        self.product.company_id = self.company_2
        tmpl = self.product.product_tmpl_id
        self.assertEqual(tmpl.company_id, self.company_2)
        self._create_po(5.0, company=self.company_2)
        self._update_product_avg_prices()
        self.assertEqual(tmpl.with_company(self.company_1).average_purchase_price, 0.0)
        self.assertEqual(tmpl.with_company(self.company_2).average_purchase_price, 5.0)

    def test_average_purchase_price_monocompany_multicurrency(self):
        self.env["res.currency.rate"].create(
            {
                "currency_id": self.other_currency.id,
                "rate": 0.5,
                "company_id": self.company_1.id,
            }
        )
        self.env["res.currency.rate"].create(
            {
                "currency_id": self.currency.id,
                "rate": 1.0,
                "company_id": self.company_1.id,
            }
        )
        self._create_po(3.0)
        self._create_po(7.0, currency=self.other_currency)
        self._update_product_avg_prices()
        # 14 + 3 / 2 = 8.5
        self.assertAlmostEqual(self.product.average_purchase_price, 8.5, places=2)
