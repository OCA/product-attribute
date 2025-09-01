# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestProductPricelistDirectPrintXLSX(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
