# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestProductPrintCategory(TransactionCase):
    """Tests for 'Product Print Category' Module"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductPrintWizard = cls.env["product.print.wizard"]
        cls.ProductProduct = cls.env["product.product"]
        cls.ProductTemplate = cls.env["product.template"]
        cls.CustomReport = cls.env["report.product_print_category.report_pricetag"]

        # 1. Create QWeb Views
        views = cls.env["ir.ui.view"].create(
            [
                {"name": f"QWeb {i}", "type": "qweb", "arch": f"<t t-name='qw_{i}'/>"}
                for i in (1, 2)
            ]
        )

        # 2. Create Product Categories
        cats = cls.env["product.category"].create(
            [{"name": n} for n in ("Root", "Consumable", "Parent", "Child")]
        )
        cats[1].parent_id = cats[2].parent_id = cats[0].id
        cats[3].parent_id = cats[2].id
        cls.root_categ, cls.consumable_categ, cls.parent_categ, cls.child_categ = cats

        # 3. Create Print Categories with triggering fields
        trigger_fields = cls.env["ir.model.fields"].search(
            [("model", "=", "product.product"), ("name", "in", ("name", "list_price"))]
        )
        cls.print_category_1, cls.print_category_2 = cls.env[
            "product.print.category"
        ].create(
            [
                {
                    "name": f"PC {i + 1}",
                    "qweb_view_id": views[i].id,
                    "field_ids": [(6, 0, trigger_fields.ids)],
                }
                for i in (0, 1)
            ]
        )

        # 4. Create Rules
        cls.env["product.print.category.rule"].create(
            [
                {
                    "sequence": 1,
                    "main_category_id": cls.parent_categ.id,
                    "print_category_id": cls.print_category_1.id,
                },
                {
                    "sequence": 2,
                    "main_category_id": cls.consumable_categ.id,
                    "print_category_id": cls.print_category_2.id,
                },
                {
                    "sequence": 100,
                    "main_category_id": cls.root_categ.id,
                    "print_category_id": False,
                },
            ]
        )

        # 5. Create basic products for test_10
        cls.env["product.product"].create(
            [
                {"name": f"P{i}", "print_category_id": cls.print_category_1.id}
                for i in (1, 2, 3)
            ]
        )

    # Test Section
    def test_01_product_product_to_print_value(self):
        product = self.ProductProduct.create(
            [
                {
                    "name": "Demo Product Product Name",
                    "print_category_id": self.print_category_1.id,
                }
            ]
        )
        self.assertEqual(product.to_print, True)

        product = self.ProductProduct.create(
            [
                {
                    "name": "Demo Product Product Name",
                }
            ]
        )
        self.assertEqual(product.to_print, False)

        product.print_category_id = self.print_category_1.id
        self.assertEqual(product.to_print, True)

        product.to_print = False
        product.name = "Demo Product Product Name Changed"
        self.assertEqual(product.to_print, True)

    def test_02_product_template_to_print_value(self):
        template = self.ProductTemplate.create(
            [
                {
                    "name": "Demo Product Product Name",
                    "print_category_id": self.print_category_1.id,
                }
            ]
        )
        self.assertEqual(template.to_print, True)

        template = self.ProductTemplate.create(
            [
                {
                    "name": "Demo Product Template Name",
                }
            ]
        )
        self.assertEqual(template.to_print, False)

        template.print_category_id = self.print_category_1.id
        self.assertEqual(template.to_print, True)

        template.to_print = False
        template.name = "Demo Product Template Name Changed"
        self.assertEqual(template.to_print, True)

    def test_10_test_wizard_obsolete(self):
        products = self.ProductProduct.search(
            [
                ("to_print", "=", True),
                ("print_category_id", "=", self.print_category_1.id),
            ]
        )
        self.assertTrue(len(products) > 0)
        wizard = self.ProductPrintWizard.with_context(
            active_model="product.print.category",
            active_ids=[self.print_category_1.id],
        ).create([{}])
        self.assertEqual(
            len(wizard.line_ids),
            len(products),
            "Print obsolete product should propose 1 product",
        )

        wizard.print_report()
        self.env.ref("product_print_category.pricetag")._render_qweb_pdf(
            "product_print_category.report_pricetag",
            wizard.line_ids.ids,
        )

        products = self.ProductProduct.search(
            [
                ("to_print", "=", True),
                ("print_category_id", "=", self.print_category_1.id),
            ]
        )
        self.assertTrue(len(products) == 0)

    def test_11_test_wizard_all(self):
        products = self.ProductProduct.search(
            [
                ("print_category_id", "=", self.print_category_1.id),
            ]
        )
        wizard = self.ProductPrintWizard.with_context(
            active_model="product.print.category",
            active_ids=[self.print_category_1.id],
            all_products=True,
        ).create({})

        self.assertEqual(
            len(wizard.line_ids),
            len(products),
            "Print all products should propose 3 products",
        )

    def test_21_onchange(self):
        product = self.ProductProduct.create(
            [
                {
                    "name": "Demo Product Product Name",
                }
            ]
        )
        self.assertEqual(product.print_category_id.id, False)

        # check rule with exact setting
        product.categ_id = self.consumable_categ
        product._onchange_categ_id_company_id()
        self.assertEqual(product.print_category_id, self.print_category_2)

        # Test with child category setting
        product.categ_id = self.child_categ
        product._onchange_categ_id_company_id()
        self.assertEqual(product.print_category_id, self.print_category_1)

        # Test if fallback settings works
        product.categ_id = self.root_categ
        product._onchange_categ_id_company_id()
        self.assertEqual(product.print_category_id.id, False)

    def test_30_product_print_category_computes(self):
        category = self.print_category_1
        # Test _compute_product_qty
        self.assertTrue(category.product_qty > 0)
        # Test _compute_to_print
        self.assertTrue(category.product_to_print_qty > 0)
        self.assertTrue(len(category.product_to_print_ids) > 0)

        # Test action_view_product_product
        action = category.action_view_product_product()
        self.assertEqual(action["domain"], [("print_category_id", "=", category.id)])

        # Test action_view_product_product with to_print context
        action_to_print = category.with_context(
            to_print=True
        ).action_view_product_product()
        self.assertTrue("to_print" in str(action_to_print["domain"]))

    def test_31_product_template_onchanges(self):
        template = self.ProductTemplate.create({"name": "Test Template Onchange"})
        template.categ_id = self.consumable_categ
        template._onchange_categ_id_company_id()
        self.assertEqual(template.print_category_id, self.print_category_2)

        template.print_category_id = False
        template.onchange_print_category_id()
        self.assertFalse(template.to_print)

    def test_32_product_product_onchanges(self):
        product = self.ProductProduct.create({"name": "Test Product Onchange"})
        product.print_category_id = False
        product.onchange_print_category_id()
        self.assertFalse(product.to_print)

        # Test rule with no category
        product.categ_id = False
        rule = self.env["product.print.category.rule"].get_print_category_rule(product)
        self.assertFalse(rule)

    def test_33_template_multiple_variants(self):
        # Create template with multiple variants to hit the else branches in computes
        attribute = self.env["product.attribute"].create({"name": "Size"})
        val1 = self.env["product.attribute.value"].create(
            {"name": "S", "attribute_id": attribute.id}
        )
        val2 = self.env["product.attribute.value"].create(
            {"name": "M", "attribute_id": attribute.id}
        )

        template = self.ProductTemplate.create(
            {
                "name": "Template Multiple Variants",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attribute.id,
                            "value_ids": [(6, 0, [val1.id, val2.id])],
                        },
                    )
                ],
            }
        )
        # Check that computes for multiple variants set values to False
        self.assertFalse(template.print_category_id)
        self.assertFalse(template.to_print)

    def test_40_wizard_other_models(self):
        # Test wizard with product.product active_model
        product = self.ProductProduct.search(
            [("print_category_id", "=", self.print_category_1.id)], limit=1
        )
        wizard_product = self.ProductPrintWizard.with_context(
            active_model="product.product", active_ids=[product.id]
        ).create({})
        self.assertEqual(len(wizard_product.line_ids), 1)

        # Test wizard with product.template active_model
        template = product.product_tmpl_id
        wizard_template = self.ProductPrintWizard.with_context(
            active_model="product.template", active_ids=[template.id]
        ).create({})
        self.assertTrue(len(wizard_template.line_ids) >= 1)

        # Test wizard with invalid model
        wizard_invalid = self.ProductPrintWizard.with_context(
            active_model="invalid.model", active_ids=[template.id]
        ).create({})
        self.assertEqual(len(wizard_invalid.line_ids), 0)

    def test_41_wizard_validation_and_prepare(self):
        from odoo.exceptions import ValidationError

        product = self.ProductProduct.create(
            {"name": "No Category Product", "print_category_id": False}
        )
        wizard = self.ProductPrintWizard.with_context(
            active_model="product.product", active_ids=[product.id]
        ).create({})

        with self.assertRaises(ValidationError):
            wizard.print_report()

        # Test _prepare_product_data
        # We manually add a line with same product to test quantity aggregation
        wizard.write(
            {
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "print_category_id": self.print_category_1.id,
                            "quantity": 2,
                        },
                    )
                ]
            }
        )
        product_data = wizard._prepare_product_data()
        self.assertEqual(
            product_data[product.id], 3
        )  # 1 from default + 2 manually added

    def test_50_mixin_invalid_model(self):
        # Test mixin NotImplementedError by calling write directly
        # on the abstract model, which will raise since it's not
        # product.product or product.template.
        mixin = self.env["product.print.category.mixin"]
        with self.assertRaises(NotImplementedError):
            mixin.write({"name": "test"})
