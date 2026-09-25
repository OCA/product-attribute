# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestProductMultiPrice(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.price_name_obj = cls.env["product.multi.price.name"]
        cls.price_field_1 = cls.price_name_obj.create({"name": "test_field_1"})
        cls.price_field_2 = cls.price_name_obj.create({"name": "test_field_2"})
        prod_tmpl_obj = cls.env["product.template"]
        cls.prod_1 = prod_tmpl_obj.create(
            {
                "name": "Test Product Template",
                "price_ids": [
                    (0, 0, {"name": cls.price_field_1.id, "price": 5.5}),
                    (0, 0, {"name": cls.price_field_2.id, "price": 20.0}),
                ],
            }
        )
        cls.prod_att_1 = cls.env["product.attribute"].create({"name": "Color"})
        cls.prod_attr1_v1 = cls.env["product.attribute.value"].create(
            {"name": "red", "attribute_id": cls.prod_att_1.id}
        )
        cls.prod_attr1_v2 = cls.env["product.attribute.value"].create(
            {"name": "blue", "attribute_id": cls.prod_att_1.id}
        )
        cls.prod_2 = prod_tmpl_obj.create(
            {
                "name": "Test Product 2 With Variants",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.prod_att_1.id,
                            "value_ids": [
                                (6, 0, [cls.prod_attr1_v1.id, cls.prod_attr1_v2.id])
                            ],
                        },
                    )
                ],
            }
        )
        cls.prod_prod_2_1 = cls.prod_2.product_variant_ids[0]
        cls.prod_prod_2_2 = cls.prod_2.product_variant_ids[1]
        cls.prod_prod_2_1.write(
            {
                "price_ids": [
                    (0, 0, {"name": cls.price_field_1.id, "price": 6.6}),
                    (0, 0, {"name": cls.price_field_2.id, "price": 7.7}),
                ],
            }
        )
        cls.prod_prod_2_2.write(
            {
                "price_ids": [
                    (0, 0, {"name": cls.price_field_1.id, "price": 8.8}),
                    (0, 0, {"name": cls.price_field_2.id, "price": 9.9}),
                ],
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test pricelist",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "compute_price": "formula",
                            "base": "multi_price",
                            "multi_price_name": cls.price_field_1.id,
                            "price_discount": 10,
                            "applied_on": "3_global",
                        },
                    )
                ],
            }
        )

    def test_product_multi_price_pricelist(self):
        """Pricelists based on multi prices for templates or variants"""
        price = self.pricelist.with_context(
            pricelist=self.pricelist.id
        )._get_products_price(self.prod_1, 1)
        self.assertAlmostEqual(price.get(self.prod_1.id), 4.95)
        price = self.pricelist.with_context(
            pricelist=self.pricelist.id
        )._get_products_price(self.prod_prod_2_1, 1)
        self.assertAlmostEqual(price.get(self.prod_prod_2_1.id), 5.94)
        price = self.pricelist.with_context(
            pricelist=self.pricelist.id
        )._get_products_price(self.prod_prod_2_2, 1)
        self.assertAlmostEqual(price.get(self.prod_prod_2_2.id), 7.92)

    def test_product_multi_price_percentage_rule(self):
        """A percentage rule on a multi price base starts from the multi price"""
        pricelist = self.env["product.pricelist"].create(
            {
                "name": "Test percentage pricelist",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "compute_price": "percentage",
                            "base": "multi_price",
                            "multi_price_name": self.price_field_2.id,
                            "percent_price": 10,
                            "applied_on": "3_global",
                        },
                    )
                ],
            }
        )
        price = pricelist._get_products_price(self.prod_1, 1)
        self.assertAlmostEqual(price.get(self.prod_1.id), 18.0)
        price = pricelist._get_products_price(self.prod_prod_2_2, 1)
        self.assertAlmostEqual(price.get(self.prod_prod_2_2.id), 8.91)

    def test_product_multi_price_pricelist_other_uom(self):
        """A formula rule prices a line in another unit of measure"""
        dozen = self.env.ref("uom.product_uom_dozen")
        price = self.pricelist._get_products_price(self.prod_1, 1, uom=dozen)
        self.assertAlmostEqual(price.get(self.prod_1.id), 59.4)

    def test_product_multi_price_base_price(self):
        """The base price of a multi price rule is the multi price itself, in the
        unit of measure asked for: sale shows it as price before discount"""
        rule = self.pricelist.item_ids
        dozen = self.env.ref("uom.product_uom_dozen")
        product = self.prod_1.product_variant_ids
        base_price = rule._compute_base_price(
            product, 1, dozen, fields.Date.today(), self.pricelist.currency_id
        )
        self.assertAlmostEqual(base_price, 66.0)

    def test_product_multi_price_pricelist_other_currency(self):
        """A formula rule converts the multi price to the pricelist currency"""
        currency = self.env["res.currency"].create(
            {
                "name": "MPT",
                "symbol": "T",
                "rate_ids": [(0, 0, {"name": "2000-01-01", "rate": 2.0})],
            }
        )
        pricelist = self.pricelist.copy({"currency_id": currency.id})
        price = pricelist._get_products_price(self.prod_1, 1)
        expected = self.prod_1.currency_id._convert(
            5.5, currency, self.env.company, fields.Date.today(), round=False
        )
        self.assertAlmostEqual(price.get(self.prod_1.id), expected * 0.9)

    def test_product_multi_price_create_multi(self):
        """Prices given on a batch create reach each single variant"""
        templates = self.env["product.template"].create(
            [
                {
                    "name": "Batch Product %s" % i,
                    "price_ids": [
                        (0, 0, {"name": self.price_field_1.id, "price": i}),
                        (0, 0, {"name": self.price_field_2.id, "price": i * 10}),
                    ],
                }
                for i in range(1, 4)
            ]
            + [{"name": "Batch Product Without Prices"}]
        )
        self.assertEqual(len(templates), 4)
        for i, template in enumerate(templates[:3], start=1):
            prices = template.product_variant_ids.price_ids
            self.assertEqual(
                sorted(prices.mapped(lambda p: (p.name.id, p.price))),
                sorted([(self.price_field_1.id, i), (self.price_field_2.id, i * 10)]),
            )
            self.assertEqual(template.price_ids, prices)
        self.assertFalse(templates[3].product_variant_ids.price_ids)

    def test_product_multi_price_of_another_company(self):
        """A price of a company the user has not selected is still found"""
        company_b = self.env["res.company"].create({"name": "Multi Price Company B"})
        price_name_b = self.price_name_obj.create(
            {"name": "test_field_b", "company_id": company_b.id}
        )
        product = self.prod_1.product_variant_ids
        product.write({"price_ids": [(0, 0, {"name": price_name_b.id, "price": 3.0})]})
        pricelist_b = self.env["product.pricelist"].create(
            {
                "name": "Company B pricelist",
                "company_id": company_b.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "compute_price": "formula",
                            "base": "multi_price",
                            "multi_price_name": price_name_b.id,
                            "applied_on": "3_global",
                        },
                    )
                ],
            }
        )
        rule = pricelist_b.item_ids
        user = self.env["res.users"].create(
            {
                "name": "Multi Price User",
                "login": "multi_price_user",
                "company_id": self.env.company.id,
                "company_ids": [(6, 0, (self.env.company | company_b).ids)],
                "groups_id": [(6, 0, self.env.ref("base.group_user").ids)],
            }
        )
        self.env.invalidate_all()
        user_product = product.with_user(user).with_context(
            allowed_company_ids=self.env.company.ids
        )
        self.assertEqual(
            user_product.price_ids.name, self.price_field_1 | self.price_field_2
        )
        self.assertAlmostEqual(user_product._get_multiprice_base_price(rule), 3.0)
