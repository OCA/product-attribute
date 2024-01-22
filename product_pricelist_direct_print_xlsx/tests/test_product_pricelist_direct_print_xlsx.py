# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProductPricelistDirectPrintXLSX(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # # Set report layout to void to wizard selection layout crashes the test
        # report_layout = cls.env.ref("web.report_layout_standard")
        # main_company = cls.env.ref("base.main_company")
        # main_company.external_report_layout_id = report_layout.view_id.id

        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Pricelist for test",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "percent_price": 5.00,
                            "compute_price": "percentage",
                        },
                    )
                ],
            }
        )

        cls.wiz_obj = cls.env["product.pricelist.print"]

    def test_report(self):
        wiz = self.wiz_obj.with_context(
            active_model="product.pricelist",
            active_id=self.pricelist.id,
        ).create({})
        report_xlsx = self.env["ir.actions.report"]._render(
            "product_pricelist_direct_print_xlsx.report", wiz.ids
        )
        self.assertGreaterEqual(len(report_xlsx[0]), 1)
        self.assertEqual(report_xlsx[1], "xlsx")
