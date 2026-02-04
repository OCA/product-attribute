# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


@tagged("post_install", "-at_install")
class TestProductPricelistDirectPrint(TransactionCase):
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

    def test_defaults(self):
        wiz = self.wiz_obj.new()
        res = wiz.with_context(
            active_model="product.pricelist", active_id=self.pricelist.id
        ).default_get([])
        self.assertEqual(res["pricelist_id"], self.pricelist.id)
        res = wiz.with_context(
            active_model="product.pricelist.item",
            active_ids=self.pricelist.item_ids.ids,
        ).default_get([])
        self.assertEqual(res["pricelist_id"], self.pricelist.id)
        res = wiz.with_context(
            active_model="res.partner",
            active_id=self.partner.id,
            active_ids=[self.partner.id],
        ).default_get([])
        self.assertEqual(
            res["pricelist_id"], self.partner.property_product_pricelist.id
        )
        res = wiz.with_context(
            active_model="product.template", active_ids=self.product.product_tmpl_id.ids
        ).default_get([])
        self.assertEqual(
            res["product_tmpl_ids"][0][2], self.product.product_tmpl_id.ids
        )
        res = wiz.with_context(
            active_model="product.product", active_ids=self.product.ids
        ).default_get([])
        self.assertEqual(res["product_ids"][0][2], self.product.ids)
        self.assertTrue(res["show_variants"])
        with self.assertRaises(ValidationError):
            wiz.print_report()
        wiz.show_sale_price = True
        res = wiz.print_report()
        self.assertIn("report_name", res)

    def test_action_pricelist_send_multiple_partner(self):
        partner_2 = self.env["res.partner"].create(
            {
                "name": "Partner for test 2",
                "property_product_pricelist": self.pricelist.id,
                "email": "test2@test.com",
            }
        )
        wiz = self.wiz_obj.with_context(
            active_model="res.partner", active_ids=[self.partner.id, partner_2.id]
        ).create({})
        wiz.action_pricelist_send()

    def test_last_ordered_products(self):
        SaleOrder = self.env["sale.order"]
        product2 = self.env["product.product"].create(
            {
                "name": "Product2 for test",
                "categ_id": self.category.id,
                "default_code": "TESTPROD02",
            }
        )
        so = self.env["sale.order"].new(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product.name,
                            "product_id": self.product.id,
                            "product_uom_qty": 10.0,
                            "product_uom": self.product.uom_id.id,
                            "price_unit": 1000.00,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": product2.name,
                            "product_id": product2.id,
                            "product_uom_qty": 10.0,
                            "product_uom": product2.uom_id.id,
                            "price_unit": 300.00,
                        },
                    ),
                ],
            }
        )
        sale_order = SaleOrder.create(so._convert_to_write(so._cache))
        sale_order.action_confirm()

        wiz = self.wiz_obj.with_context(
            active_model="res.partner", active_ids=self.partner.ids
        ).create({"last_ordered_products": 2})
        products = wiz.get_last_ordered_products_to_print()
        self.assertEqual(len(products), 2)

        wiz = self.wiz_obj.with_context(
            active_model="res.partner", active_ids=self.partner.ids
        ).create({"last_ordered_products": 1})
        products = wiz.get_last_ordered_products_to_print()
        self.assertEqual(len(products), 1)

    def test_show_only_defined_products(self):
        self.pricelist.item_ids.write(
            {"applied_on": "0_product_variant", "product_id": self.product.id}
        )
        wiz = self.wiz_obj.with_context(
            active_model="product.pricelist",
            active_id=self.pricelist.id,
        ).create({})
        wiz.show_only_defined_products = True
        wiz.show_variants = True
        products = wiz.get_products_to_print()
        self.assertIn(products, self.pricelist.item_ids.mapped("product_id"))
        self.pricelist.item_ids.write(
            {"applied_on": "2_product_category", "categ_id": self.category.id}
        )
        wiz.show_only_defined_products = True
        wiz.show_variants = True
        products = wiz.get_products_to_print()
        self.assertIn(self.product, products)

    def test_parent_categories(self):
        product_category_child = self.env["product.template"].create(
            {
                "name": "Product for test 2",
                "categ_id": self.category_child.id,
                "default_code": "TESTPROD02",
            }
        )
        self.pricelist.item_ids.write(
            {"applied_on": "2_product_category", "categ_id": self.category_child.id}
        )
        wiz = self.wiz_obj.with_context(
            active_model="product.pricelist",
            active_id=self.pricelist.id,
        ).create({})
        wiz.max_categ_level = 1
        groups = wiz.get_groups_to_print()
        product_ids = False
        for group in groups:
            if group["group_name"] == "Test category":
                product_ids = group["products"]
        self.assertTrue(product_ids)
        self.assertIn(product_category_child.id, product_ids.ids)

    def test_report(self):
        wiz = self.wiz_obj.with_context(
            active_model="product.pricelist",
            active_id=self.pricelist.id,
        ).create({})
        # Print PDF
        report_pdf = self.env.ref(
            "product_pricelist_direct_print.action_report_product_pricelist"
        )._render_qweb_pdf(
            "product_pricelist_direct_print.report_product_pricelist", wiz.ids
        )
        self.assertGreaterEqual(len(report_pdf[0]), 1)
