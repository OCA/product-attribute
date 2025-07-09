# Copyright 2025 Akretion (https://www.akretion.com).
# @author Mathieu DELVA <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests import SavepointCase


class TestPricelist(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tmpl = cls.env["product.template"].create(
            {"name": "Foo", "default_code": "test_pricelist", "lst_price": 5}
        )
        cls.tmpl2 = cls.env["product.template"].create(
            {"name": "Foo2", "default_code": "1234", "lst_price": 5}
        )
        cls.variant = cls.tmpl.product_variant_ids
        cls.variant2 = cls.tmpl2.product_variant_ids
        cls.public_pricelist = cls.env.ref("product.list0")

        cls.sale_id = cls.env.ref("sale.sale_order_18")

    def test_pricelist_filter(self):
        self.public_pricelist.item_ids = [
            (
                0,
                0,
                {
                    "applied_on": "3_global",
                    "filter_domain": "[['default_code','ilike','test']]",
                    "fixed_price": 10,
                },
            )
        ]
        self.sale_id.order_line = [
            [
                0,
                0,
                {
                    "product_id": self.variant.id,
                    "product_uom_qty": 1,
                },
            ],
            [
                0,
                0,
                {
                    "product_id": self.tmpl2.product_variant_ids.id,
                    "product_uom_qty": 1,
                },
            ],
        ]
        self.sale_id.update_prices()
        order_line = self.sale_id.order_line.filtered(
            lambda r: r.product_id == self.variant
        )
        order_line2 = self.sale_id.order_line.filtered(
            lambda r: r.product_id == self.variant2
        )
        self.assertEqual(order_line.price_unit, 10)
        self.assertEqual(order_line2.price_unit, 5)

    def test_pricelist_without_filter(self):
        self.public_pricelist.item_ids = [(5, 0, 0)]
        self.sale_id.order_line = [
            (
                0,
                0,
                {
                    "product_id": self.variant.id,
                    "product_uom_qty": 1,
                },
            )
        ]
        order_line = self.sale_id.order_line.filtered(
            lambda r: r.product_id == self.variant
        )
        self.assertEqual(order_line.price_unit, self.variant.lst_price)
