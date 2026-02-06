"""
Test UC3: Packaging Views & Navigation

As a warehouse planner, I want standalone views for packaging configurations
so that I can browse, search, and manage them outside of the product form.

Acceptance Criteria:
- Standalone form view exposes all key fields (name, product, UoM, qty,
  package type, sequence, company)
- Search view allows filtering by product, UoM, and package type
- Menu action exists under Inventory > Configuration
- Fields are editable via the standalone form
"""

from lxml import etree

from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestUC3PackagingViews(TransactionCase):
    """Test UC3: Packaging Views & Navigation"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductUomPackaging = cls.env["product.uom.packaging"]

        cls.product = cls.env["product.product"].create({"name": "Product A"})
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")
        cls.package_small = cls.env["stock.package.type"].create(
            {
                "name": "Small Box",
                "packaging_length": 10,
                "width": 10,
                "height": 10,
                "base_weight": 0.5,
                "max_weight": 10,
            }
        )

    def test_form_view_has_expected_fields(self):
        """UC3: Standalone form view exposes all key fields."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
            }
        )
        with Form(packaging) as f:
            self.assertTrue(hasattr(f, "name"))
            self.assertTrue(hasattr(f, "product_tmpl_id"))
            self.assertTrue(hasattr(f, "uom_id"))
            self.assertTrue(hasattr(f, "qty"))
            self.assertTrue(hasattr(f, "package_type_id"))
            self.assertTrue(hasattr(f, "sequence"))

    def test_form_view_fields_are_editable(self):
        """UC3: Key fields can be edited via the standalone form."""
        packaging = self.ProductUomPackaging.create(
            {
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "uom_id": self.uom_unit.id,
                "package_type_id": self.package_small.id,
            }
        )
        with Form(packaging) as f:
            f.name = "Custom Name"
            f.uom_id = self.uom_dozen
            f.qty = 24.0
            f.sequence = 5

        self.assertEqual(packaging.name, "Custom Name")
        self.assertEqual(packaging.uom_id, self.uom_dozen)
        self.assertEqual(packaging.qty, 24.0)
        self.assertEqual(packaging.sequence, 5)

    def test_search_view_has_filter_fields(self):
        """UC3: Search view allows filtering by product, UoM, and package type."""
        views = self.ProductUomPackaging.get_views(
            [(False, "search")],
        )
        arch = etree.fromstring(views["views"]["search"]["arch"])
        field_names = [f.get("name") for f in arch.findall(".//field")]
        self.assertIn("product_tmpl_id", field_names)
        self.assertIn("uom_id", field_names)
        self.assertIn("package_type_id", field_names)

    def test_list_view_has_expected_columns(self):
        """UC3: List view shows name, product, UoM, qty, and package type."""
        views = self.ProductUomPackaging.get_views(
            [(False, "list")],
        )
        arch = etree.fromstring(views["views"]["list"]["arch"])
        field_names = [f.get("name") for f in arch.findall(".//field")]
        for expected in ("name", "product_tmpl_id", "uom_id", "qty", "package_type_id"):
            self.assertIn(expected, field_names)

    def test_menu_action_exists(self):
        """UC3: Menu action opens the packaging list/form views."""
        action = self.env.ref("product_uom_packaging.product_uom_packaging_action")
        self.assertEqual(action.res_model, "product.uom.packaging")
        self.assertIn("list", action.view_mode)
        self.assertIn("form", action.view_mode)
