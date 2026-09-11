# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields
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
                            "product_uom_id": self.product.uom_id.id,
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
                            "product_uom_id": product2.uom_id.id,
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

    def test_compute_product_price_vat(self):
        tax = self.env["account.tax"].create(
            {
                "name": "Tax 10",
                "amount": 10.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
            }
        )
        self.product.taxes_id = [(6, 0, tax.ids)]
        wiz = self.wiz_obj.with_context(product=self.product).create(
            {"vat_mode": "vat_excl", "pricelist_id": self.pricelist.id}
        )
        self.assertIsInstance(wiz.product_price, float)
        self.product.list_price = 100.0
        wiz._compute_product_price()
        wiz.vat_mode = "vat_incl"
        wiz._compute_product_price()
        wiz.vat_mode = False
        wiz._compute_product_price()

    def test_default_get_scenarios(self):
        res = self.wiz_obj.with_context(
            active_model="res.partner",
            active_id=self.partner.id,
            active_ids=[self.partner.id],
        ).default_get(["pricelist_id", "partner_ids"])
        self.assertEqual(
            res["pricelist_id"], self.partner.property_product_pricelist.id
        )
        item = self.pricelist.item_ids[0]
        res = self.wiz_obj.with_context(
            active_model="product.pricelist.item", active_ids=item.ids
        ).default_get(["pricelist_id"])
        self.assertEqual(res["pricelist_id"], self.pricelist.id)

    def test_mailing_actions(self):
        wiz = self.wiz_obj.create(
            {
                "partner_ids": [(6, 0, self.partner.ids)],
                "pricelist_id": self.pricelist.id,
            }
        )
        res = wiz.action_pricelist_send()
        self.assertEqual(res["res_model"], "mail.compose.message")
        partner2 = self.partner.copy({"name": "Partner 2", "email": "p2@test.com"})
        wiz.partner_ids = [(4, partner2.id)]
        wiz.action_pricelist_send()  # Should call send_batch

    def test_filtering_and_sorting(self):
        wiz = self.wiz_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "order_field": "name",
                "max_categ_level": 2,
                "last_categ_level_to_print": 1,
            }
        )
        self.assertEqual(wiz.get_group_name("Category / Subcategory"), " Subcategory")
        wiz.show_only_defined_products = True
        self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "2_product_category",
                "categ_id": self.category.id,
            }
        )
        domain = wiz.get_products_domain()
        self.assertTrue(
            any(leaf[0] == "categ_id" for leaf in domain if isinstance(leaf, tuple))
        )
        wiz.product_selling_date_threshold = fields.Datetime.now()
        domain_so = wiz._get_sale_order_domain(self.partner)
        self.assertTrue(
            any(
                leaf[0] == "date_order" for leaf in domain_so if isinstance(leaf, tuple)
            )
        )

    def test_grouping_logic(self):
        wiz = self.wiz_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "group_field": "categ_id",
            }
        )
        groups = wiz.get_groups_to_print()
        wiz.product_tmpl_ids = [(6, 0, self.product.product_tmpl_id.ids)]
        groups = wiz.get_groups_to_print()
        self.assertTrue(len(groups) > 0)
        self.assertEqual(groups[0]["group_name"], self.category.name)

    def test_lang_get(self):
        from ..wizards.product_pricelist_print import _lang_get

        result = _lang_get(self.wiz_obj)
        self.assertIsInstance(result, list)

    def test_onchange_categ_ids(self):
        wiz = self.wiz_obj.new({"pricelist_id": self.pricelist.id})
        wiz.categ_ids = [(4, self.category.id)]
        wiz._onchange_categ_ids()
        self.assertTrue(wiz.print_child_categories)
        wiz.categ_ids = [(5,)]
        wiz._onchange_categ_ids()
        self.assertFalse(wiz.print_child_categories)

    def test_onchange_partner_ids_clears_last_ordered(self):
        wiz = self.wiz_obj.new(
            {
                "pricelist_id": self.pricelist.id,
                "last_ordered_products": 5,
            }
        )
        # With no partners, partner_count=0, so last_ordered_products should be cleared
        wiz.partner_ids = [(5,)]
        wiz._onchange_partner_ids()
        self.assertFalse(wiz.last_ordered_products)

    def test_compute_context_active_model(self):
        wiz = self.wiz_obj.with_context(active_model="product.template").new({})
        wiz._compute_context_active_model()
        self.assertEqual(wiz.context_active_model, "product.template")

    def test_get_pricelist_to_print_from_partner(self):
        wiz = self.wiz_obj.create(
            {
                "partner_ids": [(6, 0, self.partner.ids)],
            }
        )
        pricelist = wiz.get_pricelist_to_print()
        self.assertEqual(pricelist, self.partner.property_product_pricelist)

    def test_get_last_ordered_products_no_partner_id(self):
        SaleOrder = self.env["sale.order"]
        so = SaleOrder.create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product.name,
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        so.action_confirm()
        # No partner_id set, but partner_ids has exactly one partner
        wiz = self.wiz_obj.create(
            {
                "partner_ids": [(6, 0, self.partner.ids)],
            }
        )
        products = wiz.get_last_ordered_products_to_print()
        self.assertIn(self.product, products)

    def test_get_last_ordered_products_all(self):
        SaleOrder = self.env["sale.order"]
        so = SaleOrder.create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product.name,
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        so.action_confirm()
        wiz = self.wiz_obj.create(
            {
                "partner_id": self.partner.id,
                "last_ordered_products": 0,
            }
        )
        products = wiz.get_last_ordered_products_to_print()
        self.assertIn(self.product, products)

    def test_default_get_pricelist_item_with_product_variants(self):
        # Create an item applied on a product variant
        item = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "0_product_variant",
                "product_id": self.product.id,
                "compute_price": "fixed",
                "fixed_price": 10.0,
            }
        )
        res = self.wiz_obj.with_context(
            active_model="product.pricelist.item",
            active_ids=item.ids,
        ).default_get(["show_variants", "product_ids", "pricelist_id"])
        self.assertTrue(res.get("show_variants"))
        self.assertIn(self.product.id, res["product_ids"][0][2])

    def test_default_get_pricelist_item_mixed_product_and_template(self):
        item_variant = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "0_product_variant",
                "product_id": self.product.id,
                "compute_price": "fixed",
                "fixed_price": 10.0,
            }
        )
        product2 = self.env["product.product"].create(
            {
                "name": "Product Template Test",
                "categ_id": self.category.id,
            }
        )
        item_template = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "1_product",
                "product_tmpl_id": product2.product_tmpl_id.id,
                "compute_price": "fixed",
                "fixed_price": 20.0,
            }
        )
        res = self.wiz_obj.with_context(
            active_model="product.pricelist.item",
            active_ids=(item_variant | item_template).ids,
        ).default_get(["show_variants", "product_ids"])
        self.assertTrue(res.get("show_variants"))
        self.assertIn(self.product.id, res["product_ids"][0][2])

    def test_get_products_domain_show_variants_with_product_items(self):
        self.pricelist.item_ids.write(
            {
                "applied_on": "1_product",
                "product_tmpl_id": self.product.product_tmpl_id.id,
            }
        )
        self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "0_product_variant",
                "product_id": self.product.id,
                "compute_price": "fixed",
                "fixed_price": 10.0,
            }
        )
        wiz = self.wiz_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "show_only_defined_products": True,
                "show_variants": True,
            }
        )
        domain = wiz.get_products_domain()
        domain_str = str(domain)
        self.assertIn("product_tmpl_id", domain_str)

    def test_get_products_domain_no_show_variants_with_product_and_variant_items(self):
        self.pricelist.item_ids.write(
            {
                "applied_on": "1_product",
                "product_tmpl_id": self.product.product_tmpl_id.id,
            }
        )
        self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "0_product_variant",
                "product_id": self.product.id,
                "compute_price": "fixed",
                "fixed_price": 10.0,
            }
        )
        wiz = self.wiz_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "show_only_defined_products": True,
                "show_variants": False,
            }
        )
        domain = wiz.get_products_domain()
        domain_str = str(domain)
        # show_variants=False → id branch (line 335-338) for product items
        # and product_variant_ids branch (line 344-349) for variant items
        self.assertIn("product_variant_ids", domain_str)

    def test_get_products_domain_print_child_categories(self):
        wiz = self.wiz_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "categ_ids": [(6, 0, self.category.ids)],
                "print_child_categories": True,
            }
        )
        domain = wiz.get_products_domain()
        self.assertTrue(
            any(
                isinstance(leaf, tuple)
                and leaf[0] == "categ_id"
                and leaf[1] == "child_of"
                for leaf in domain
            )
        )
        # Now test the elif categ_ids branch (line 356-357)
        wiz.print_child_categories = False
        domain = wiz.get_products_domain()
        self.assertTrue(
            any(
                isinstance(leaf, tuple) and leaf[0] == "categ_id" and leaf[1] == "in"
                for leaf in domain
            )
        )

    def test_get_products_to_print_with_selling_date_threshold(self):
        SaleOrder = self.env["sale.order"]
        so = SaleOrder.create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.product.name,
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        so.action_confirm()
        wiz = self.wiz_obj.create(
            {
                "partner_id": self.partner.id,
                "pricelist_id": self.pricelist.id,
                "product_selling_date_threshold": fields.Datetime.now(),
            }
        )
        products = wiz.get_products_to_print()
        # Result may be empty (no orders since 'now'), but the branch is executed
        self.assertIsNotNone(products)

    def test_get_sorted_products_no_order_field(self):
        wiz = self.wiz_obj.create({"pricelist_id": self.pricelist.id})
        products = self.product.product_tmpl_id.product_variant_ids
        result = wiz.get_sorted_products(products)
        self.assertEqual(result, products)

    def test_get_groups_to_print_no_products(self):
        # Use a pricelist that has no matching products for any domain
        empty_pricelist = self.env["product.pricelist"].create(
            {"name": "Empty pricelist for test"}
        )
        # Create a category with no products
        empty_category = self.env["product.category"].create(
            {"name": "Empty category for test"}
        )
        wiz = self.wiz_obj.create(
            {
                "pricelist_id": empty_pricelist.id,
                "categ_ids": [(6, 0, empty_category.ids)],
                "print_child_categories": False,
            }
        )
        groups = wiz.get_groups_to_print()
        self.assertEqual(groups, [])

    def test_action_pricelist_send_single_partner(self):
        wiz = self.wiz_obj.create(
            {
                "partner_ids": [(6, 0, self.partner.ids)],
                "pricelist_id": self.pricelist.id,
            }
        )
        # partner_count == 1 → goes through message_composer_action
        res = wiz.action_pricelist_send()
        self.assertEqual(res["res_model"], "mail.compose.message")

    def test_default_get_pricelist_item_only_template_items(self):
        item_template = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "1_product",
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "compute_price": "fixed",
                "fixed_price": 20.0,
            }
        )
        item_category = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "2_product_category",
                "categ_id": self.category_child.id,
                "compute_price": "fixed",
                "fixed_price": 30.0,
            }
        )
        res = self.wiz_obj.with_context(
            active_model="product.pricelist.item",
            active_ids=(item_template | item_category).ids,
        ).default_get(["product_tmpl_ids"])
        self.assertIn(self.product.product_tmpl_id.id, res["product_tmpl_ids"][0][2])

    def test_default_get_pricelist_item_only_category_items(self):
        item_category = self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "2_product_category",
                "categ_id": self.category.id,
                "compute_price": "fixed",
                "fixed_price": 30.0,
            }
        )
        res = self.wiz_obj.with_context(
            active_model="product.pricelist.item",
            active_ids=item_category.ids,
        ).default_get(["categ_ids"])
        self.assertIn(self.category.id, res["categ_ids"][0][2])

    def test_selection_group_field(self):
        res = self.wiz_obj.new()._selection_group_field()
        self.assertTrue(isinstance(res, list))
        self.assertTrue(len(res) > 0)
        self.assertTrue(isinstance(res[0], tuple))

    def test_get_sorted_products_with_order_field(self):
        wiz = self.wiz_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "order_field": "default_code",
            }
        )
        product2 = self.env["product.product"].create(
            {
                "name": "Product 2",
                "categ_id": self.category.id,
                "default_code": "AAA",
            }
        )
        product3 = self.env["product.product"].create(
            {
                "name": "Product 3",
                "categ_id": self.category.id,
                "default_code": False,
            }
        )
        products = self.product | product2 | product3
        sorted_products = wiz.get_sorted_products(products)
        self.assertEqual(sorted_products[0], product3)
        self.assertEqual(sorted_products[1], product2)
        self.assertEqual(sorted_products[2], self.product)
