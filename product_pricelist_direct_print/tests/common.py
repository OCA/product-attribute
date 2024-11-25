# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


@tagged("-at_install", "post_install")
class Common(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        # Set report layout to void to wizard selection layout crashes the test
        report_layout = cls.env.ref("web.report_layout_standard")
        main_company = cls.env.ref("base.main_company")
        main_company.external_report_layout_id = report_layout.view_id.id

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
        cls.category = cls.env["product.category"].create({"name": "Test category"})
        cls.category_child = cls.env["product.category"].create(
            {"name": "Test category child", "parent_id": cls.category.id}
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product for test",
                "categ_id": cls.category.id,
                "default_code": "TESTPROD01",
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Partner for test",
                "property_product_pricelist": cls.pricelist.id,
                "email": "test@test.com",
            }
        )
        cls.wiz_obj = cls.env["product.pricelist.print"]
