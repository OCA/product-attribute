# Copyright 2025 Akretion (https://www.akretion.com).
# @author Mathieu DELVA <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command
from odoo.tests import TransactionCase


class TestPricelist(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["res.config.settings"].create(
            {
                "group_product_pricelist": True,
            }
        ).execute()
        cls.tmpl = cls.env["product.template"].create(
            {"name": "Foo", "default_code": "test_pricelist", "list_price": 5}
        )
        cls.tmpl2 = cls.env["product.template"].create(
            {"name": "Foo2", "default_code": "1234", "list_price": 5}
        )
        cls.variant = cls.tmpl.product_variant_ids
        cls.variant.default_code = "test_pricelist"
        cls.variant2 = cls.tmpl2.product_variant_ids
        cls.variant2.default_code = "1234"
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test Pricelist",
            }
        )
        cls.partner_id = cls.env.ref("base.res_partner_4")
        cls.sale_id = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_id.id,
                "pricelist_id": cls.pricelist.id,
            }
        )

    def test_pricelist_filter(self):
        self.pricelist.item_ids = [
            Command.create(
                {
                    "applied_on": "3_global",
                    "filter_domain": "[['default_code', 'ilike', 'test']]",
                    "fixed_price": 10,
                }
            )
        ]
        self.sale_id.order_line = [
            Command.create(
                {
                    "product_id": self.variant.id,
                    "product_uom_qty": 1,
                }
            ),
            Command.create(
                {
                    "product_id": self.variant2.id,
                    "product_uom_qty": 1,
                }
            ),
        ]

        order_line = self.sale_id.order_line.filtered(
            lambda r: r.product_id == self.variant
        )
        order_line2 = self.sale_id.order_line.filtered(
            lambda r: r.product_id == self.variant2
        )
        self.assertEqual(order_line.product_id.default_code, "test_pricelist")
        self.assertTrue(self.sale_id.pricelist_id)
        self.assertEqual(self.sale_id.pricelist_id.name, "Test Pricelist")
        self.assertEqual(len(self.sale_id.pricelist_id.item_ids), 1)
        self.assertEqual(order_line.price_unit, 10)
        self.assertEqual(order_line2.price_unit, 5)

    def test_pricelist_without_filter(self):
        self.pricelist.item_ids = [Command.clear()]
        self.sale_id.order_line = [
            Command.create(
                {
                    "product_id": self.variant.id,
                    "product_uom_qty": 1,
                }
            )
        ]

        order_line = self.sale_id.order_line.filtered(
            lambda r: r.product_id == self.variant
        )
        self.assertEqual(order_line.price_unit, self.variant.list_price)
