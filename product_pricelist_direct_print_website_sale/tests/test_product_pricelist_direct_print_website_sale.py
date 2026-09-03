# Copyright 2024 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from unittest.mock import patch

from odoo.tests.common import tagged

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.product_pricelist_direct_print_xlsx.report import (
    product_pricelist_xlsx as xlsx_report,
)

BaseXlsx = xlsx_report.ProductPricelistXlsx


@tagged("post_install", "-at_install")
class TestProductPricelistDirectPrintWebsiteSale(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        report_layout = cls.env.ref("web.report_layout_standard")
        main_company = cls.env.ref("base.main_company")
        main_company.external_report_layout_id = report_layout.view_id.id
        cls.public_categ_a = cls.env["product.public.category"].create(
            {"name": "Website Category A"}
        )
        cls.public_categ_b = cls.env["product.public.category"].create(
            {"name": "Website Category B"}
        )
        cls.internal_categ = cls.env["product.category"].create(
            {"name": "Internal Test Category"}
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test Pricelist (Website)",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "percent_price": 10.0,
                            "compute_price": "percentage",
                        },
                    )
                ],
            }
        )
        cls.product_with_categ = cls.env["product.product"].create(
            {
                "name": "Product With Public Category",
                "categ_id": cls.internal_categ.id,
                "public_categ_ids": [(6, 0, [cls.public_categ_a.id])],
                "list_price": 100.0,
            }
        )
        cls.product_with_multi_categ = cls.env["product.product"].create(
            {
                "name": "Product With Multi Public Category",
                "categ_id": cls.internal_categ.id,
                "public_categ_ids": [
                    (6, 0, [cls.public_categ_a.id, cls.public_categ_b.id])
                ],
                "list_price": 200.0,
            }
        )
        cls.product_no_categ = cls.env["product.product"].create(
            {
                "name": "Product Without Public Category",
                "categ_id": cls.internal_categ.id,
                "public_categ_ids": [(5, 0, 0)],
                "list_price": 50.0,
            }
        )
        cls.wiz_obj = cls.env["product.pricelist.print"]

    def _get_xlsx_report_obj(self):
        return self.env["report.product_pricelist_direct_print_xlsx.report"]

    def test_new_fields_default_false(self):
        """New fields should be falsy by default."""
        wiz = self.wiz_obj.create({"pricelist_id": self.pricelist.id})
        self.assertFalse(wiz.is_public_categ)
        self.assertFalse(wiz.show_public_category)
        self.assertFalse(wiz.public_categ_ids)

    def test_get_products_domain_no_public_categ_filter(self):
        """Domain must not filter by public_categ_ids when none are selected."""
        wiz = self.wiz_obj.create(
            {"pricelist_id": self.pricelist.id, "public_categ_ids": [(5, 0, 0)]}
        )
        domain = wiz.get_products_domain()
        has_leaf = any(
            isinstance(leaf, (list, tuple)) and leaf[0] == "public_categ_ids"
            for leaf in domain
        )
        self.assertFalse(has_leaf)

    def test_get_products_domain_with_single_public_categ(self):
        """Domain must contain public_categ_ids filter when a category is selected."""
        wiz = self.wiz_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "public_categ_ids": [(6, 0, [self.public_categ_a.id])],
            }
        )
        domain = wiz.get_products_domain()
        leaves = [
            leaf
            for leaf in domain
            if isinstance(leaf, (list, tuple)) and leaf[0] == "public_categ_ids"
        ]
        self.assertTrue(leaves)
        self.assertEqual(leaves[0][1], "in")
        self.assertIn(self.public_categ_a.id, leaves[0][2])

    def test_get_products_domain_with_multiple_public_categs(self):
        """All selected public categories must appear in the domain."""
        wiz = self.wiz_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "public_categ_ids": [
                    (6, 0, [self.public_categ_a.id, self.public_categ_b.id])
                ],
            }
        )
        domain = wiz.get_products_domain()
        leaves = [
            leaf
            for leaf in domain
            if isinstance(leaf, (list, tuple)) and leaf[0] == "public_categ_ids"
        ]
        ids_in_domain = leaves[0][2]
        self.assertIn(self.public_categ_a.id, ids_in_domain)
        self.assertIn(self.public_categ_b.id, ids_in_domain)

    def test_get_products_domain_filters_actual_products(self):
        """Domain must return only products assigned to the selected category."""
        wiz = self.wiz_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "public_categ_ids": [(6, 0, [self.public_categ_a.id])],
            }
        )
        domain = wiz.get_products_domain()
        products = self.env["product.product"].search(domain)
        self.assertIn(self.product_with_categ, products)
        self.assertIn(self.product_with_multi_categ, products)
        self.assertNotIn(self.product_no_categ, products)

    def test_get_group_key_public_categ_mode_with_categ(self):
        """Group key must be the first public category name."""
        wiz = self.wiz_obj.create(
            {"pricelist_id": self.pricelist.id, "is_public_categ": True}
        )
        key = wiz.get_group_key(self.product_with_categ)
        self.assertEqual(key, self.public_categ_a.name)

    def test_get_group_key_public_categ_mode_first_categ_used(self):
        """With multiple public categories, only the first must be used."""
        wiz = self.wiz_obj.create(
            {"pricelist_id": self.pricelist.id, "is_public_categ": True}
        )
        key = wiz.get_group_key(self.product_with_multi_categ)
        self.assertEqual(key, self.product_with_multi_categ.public_categ_ids[:1].name)

    def test_get_group_key_public_categ_mode_no_categ_returns_empty_string(self):
        """Group key must be empty string when product has no public category."""
        wiz = self.wiz_obj.create(
            {"pricelist_id": self.pricelist.id, "is_public_categ": True}
        )
        self.assertEqual(wiz.get_group_key(self.product_no_categ), "")

    def test_get_group_key_falls_back_to_super_when_not_public_categ(self):
        """When is_public_categ=False, super() must handle the group key."""
        wiz = self.wiz_obj.create(
            {"pricelist_id": self.pricelist.id, "is_public_categ": False}
        )
        key = wiz.get_group_key(self.product_with_categ)
        self.assertNotEqual(key, self.public_categ_a.name)

    def test_get_groups_to_print_grouped_by_public_categ(self):
        """Groups must use public category names when is_public_categ=True."""
        wiz = self.wiz_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "is_public_categ": True,
                "product_tmpl_ids": [
                    (
                        6,
                        0,
                        [
                            self.product_with_categ.product_tmpl_id.id,
                            self.product_no_categ.product_tmpl_id.id,
                        ],
                    )
                ],
            }
        )
        group_names = [g["group_name"] for g in wiz.get_groups_to_print()]
        self.assertIn(self.public_categ_a.name, group_names)
        self.assertIn("", group_names)

    def test_get_groups_to_print_filtered_by_public_categ(self):
        """Only products in the selected public category must appear in groups."""
        wiz = self.wiz_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "public_categ_ids": [(6, 0, [self.public_categ_a.id])],
                "is_public_categ": True,
            }
        )
        all_tmpls = self.env["product.template"].browse()
        for g in wiz.get_groups_to_print():
            all_tmpls |= g["products"]
        self.assertNotIn(self.product_no_categ.product_tmpl_id, all_tmpls)

    def test_xlsx_prepare_header_row_show_public_category_true(self):
        """Public Category column must be appended when show_public_category=True."""
        wiz = self.wiz_obj.create(
            {"pricelist_id": self.pricelist.id, "show_public_category": True}
        )
        report_obj = self._get_xlsx_report_obj()
        with patch.object(
            BaseXlsx, "_prepare_header_row", return_value=[], create=True
        ):
            row = report_obj._prepare_header_row(wiz)
        self.assertIn("Public Category", row)

    def test_xlsx_prepare_header_row_show_public_category_false(self):
        """Public Category column not appended when show_public_category=False."""
        wiz = self.wiz_obj.create(
            {"pricelist_id": self.pricelist.id, "show_public_category": False}
        )
        report_obj = self._get_xlsx_report_obj()
        with patch.object(
            BaseXlsx, "_prepare_header_row", return_value=[], create=True
        ):
            row = report_obj._prepare_header_row(wiz)
        self.assertNotIn("Public Category", row)

    def test_xlsx_prepare_data_row_with_formats_show_public_category_true(self):
        """Public category display_name must be appended as (name, None) tuple."""
        wiz = self.wiz_obj.create(
            {"pricelist_id": self.pricelist.id, "show_public_category": True}
        )
        report_obj = self._get_xlsx_report_obj()
        with patch.object(
            BaseXlsx, "_prepare_data_row_with_formats", return_value=[], create=True
        ):
            row = report_obj._prepare_data_row_with_formats(
                wiz, self.product_with_categ, {}
            )
        last_cell = row[-1]
        self.assertIsInstance(last_cell, tuple)
        self.assertEqual(len(last_cell), 2)
        self.assertIsNone(last_cell[1])
        self.assertEqual(
            last_cell[0], self.product_with_categ.public_categ_ids[:1].display_name
        )

    def test_xlsx_prepare_data_row_with_formats_show_public_category_false(self):
        """No extra cell must be appended when show_public_category=False."""
        wiz = self.wiz_obj.create(
            {"pricelist_id": self.pricelist.id, "show_public_category": False}
        )
        report_obj = self._get_xlsx_report_obj()
        with patch.object(
            BaseXlsx, "_prepare_data_row_with_formats", return_value=[], create=True
        ):
            row = report_obj._prepare_data_row_with_formats(
                wiz, self.product_with_categ, {}
            )
        self.assertEqual(row, [])

    def test_xlsx_prepare_data_row_product_no_public_categ(self):
        """Appended tuple's first element must be falsy for uncategorised products."""
        wiz = self.wiz_obj.create(
            {"pricelist_id": self.pricelist.id, "show_public_category": True}
        )
        report_obj = self._get_xlsx_report_obj()
        with patch.object(
            BaseXlsx, "_prepare_data_row_with_formats", return_value=[], create=True
        ):
            row = report_obj._prepare_data_row_with_formats(
                wiz, self.product_no_categ, {}
            )
        last_cell = row[-1]
        self.assertIsInstance(last_cell, tuple)
        self.assertFalse(last_cell[0])

    def test_xlsx_report_render_with_public_category(self):
        """XLSX report must render successfully with show_public_category=True."""
        wiz = self.wiz_obj.with_context(
            active_model="product.pricelist",
            active_id=self.pricelist.id,
        ).create({"show_public_category": True, "is_public_categ": True})
        report_xlsx = self.env["ir.actions.report"]._render(
            "product_pricelist_direct_print_xlsx.report", wiz.ids
        )
        self.assertGreaterEqual(len(report_xlsx[0]), 1)
        self.assertEqual(report_xlsx[1], "xlsx")

    def test_xlsx_report_render_without_public_category(self):
        """XLSX report must render successfully with show_public_category=False."""
        wiz = self.wiz_obj.with_context(
            active_model="product.pricelist",
            active_id=self.pricelist.id,
        ).create({"show_public_category": False})
        report_xlsx = self.env["ir.actions.report"]._render(
            "product_pricelist_direct_print_xlsx.report", wiz.ids
        )
        self.assertGreaterEqual(len(report_xlsx[0]), 1)
        self.assertEqual(report_xlsx[1], "xlsx")

    def test_pdf_report_render_with_public_categ_grouping(self):
        """PDF report must render successfully with is_public_categ grouping."""
        wiz = self.wiz_obj.with_context(
            active_model="product.pricelist",
            active_id=self.pricelist.id,
        ).create(
            {
                "is_public_categ": True,
                "show_public_category": True,
                "public_categ_ids": [(6, 0, [self.public_categ_a.id])],
            }
        )
        report_pdf = self.env.ref(
            "product_pricelist_direct_print.action_report_product_pricelist"
        )._render_qweb_pdf(
            "product_pricelist_direct_print.report_product_pricelist", wiz.ids
        )
        self.assertGreaterEqual(len(report_pdf[0]), 1)
