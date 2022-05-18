# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields
from odoo.tests.common import SavepointCase


class TestProductMainSupplierInfo(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductMainSupplierInfo, cls).setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product = cls.env.ref("product.product_product_6")
        cls.seller_1 = cls.env.ref("product.product_supplierinfo_1")
        cls.seller_1.sequence = 1
        cls.seller_1.price = 700
        cls.seller_2 = cls.env.ref("product.product_supplierinfo_2")
        cls.seller_2.sequence = 2
        cls.seller_2.price = 720
        cls.seller_2bis = cls.env.ref("product.product_supplierinfo_2bis")
        cls.seller_2bis.sequence = 3
        cls.seller_2bis.price = 740
        cls.company_2 = cls.env.company.create({"name": "Company2"})
        # For the test case 4
        cls.attribute = cls.env["product.attribute"].create({"name": "Size"})
        cls.attribute_value_1 = cls.env["product.attribute.value"].create(
            {"name": "L", "attribute_id": cls.attribute.id}
        )
        cls.attribute_value_2 = cls.env["product.attribute.value"].create(
            {"name": "XL", "attribute_id": cls.attribute.id}
        )
        cls.template1 = cls.env["product.template"].create(
            {
                "name": "Hat",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attribute.id,
                            "value_ids": [
                                (
                                    6,
                                    0,
                                    [
                                        cls.attribute_value_1.id,
                                        cls.attribute_value_2.id,
                                    ],
                                )
                            ],
                        },
                    ),
                ],
            }
        )
        cls.product_1 = cls.template1.product_variant_ids[0]
        cls.product_2 = cls.template1.product_variant_ids[1]
        cls.date_old = "2000-01-01"
        cls.date_older = "2000-12-31"
        cls.product_template_supply = cls.seller_2.copy(
            {
                "product_tmpl_id": cls.product_2.product_tmpl_id.id,
                "sequence": 1,
                "date_start": cls.date_older,
                "date_end": cls.date_old,
            }
        )
        cls.product_1_supply = cls.seller_1.copy(
            {
                "product_tmpl_id": cls.product_1.product_tmpl_id.id,
                "product_id": cls.product_1.id,
                "sequence": 2,
                "date_start": cls.date_older,
                "date_end": cls.date_old,
            }
        )
        cls.product_2_supply = cls.seller_2.copy(
            {
                "product_tmpl_id": cls.product_2.product_tmpl_id.id,
                "product_id": cls.product_2.id,
                "sequence": 3,
                "date_start": cls.date_older,
                "date_end": cls.date_old,
            }
        )

    def test_main_seller_1(self):
        """ "Case 1: all the sellers share the same company."""
        self.assertEqual(self.product.main_seller_id, self.seller_1)
        self.seller_2.price = 650
        self.assertEqual(self.product.main_seller_id, self.seller_2)

    def test_main_seller_2(self):
        """ "Case 2: the sellers do not share the same company."""
        # Assign 'seller_1' to the second company, so the main vendor computed
        # for the main company is now 'seller_2'
        self.seller_1.company_id = self.company_2
        self.assertEqual(self.product.main_seller_id, self.seller_2)
        # Check that the main vendor for the second company is 'seller_1'
        self.assertEqual(
            self.product.with_company(self.company_2).main_seller_id,
            self.seller_1,
        )

    def test_main_seller_3(self):
        """ "Case 3: the sellers have different start/end dates."""
        today = fields.Date.today()
        tomorrow = fields.Date.add(today, days=1)
        yesterday = fields.Date.subtract(today, days=1)
        self.seller_1.date_start = tomorrow
        self.seller_2.date_end = yesterday
        self.assertEqual(self.product.main_seller_id, self.seller_2bis)

    def test_main_seller_4(self):
        """Case 4: No valid supplier so select one related to the variant."""
        self.assertEqual(self.product_1.main_seller_id, self.product_1_supply)
        self.assertEqual(self.product_2.main_seller_id, self.product_2_supply)
