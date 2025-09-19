# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestProuctFormList(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product 1",
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "List 1",
                "item_ids": [
                    Command.create(
                        {
                            "product_id": cls.product.id,
                            "applied_on": "0_product_variant",
                            "compute_price": "percentage",
                            "percent_price": 20.0,
                        }
                    )
                ],
            }
        )

    def test_product_pricelist(self):
        self.product.invalidate_recordset()
        self.assertEqual(self.pricelist.item_ids, self.product.pricelist_item_ids)
