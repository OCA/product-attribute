# Copyright 2021 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestProductCategoryCode(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        vals = {
            "name": "Category Test",
            "code": "XYZ",
        }
        cls.category = cls.env["product.category"].create(vals)

    def test_category(self):
        new_category = self.category.copy()

        self.assertEqual(
            "XYZ-copy",
            new_category.code,
        )

    def test_display_name(self):
        """The code is shown in the display name, unless disabled by context.

        Scenario:
            1. Read the name of a category that has a code.
            2. Read it again, asking not to show the code.
        Expected:
            - The first name starts with the code between brackets.
            - The second name is the plain category name.
        """
        self.assertEqual(self.category.display_name, "[XYZ] Category Test")
        self.assertEqual(
            self.category.with_context(display_category_code=False).display_name,
            "Category Test",
        )

    def test_display_name_without_code(self):
        """Categories with the "/" placeholder code show their plain name."""
        category = self.env["product.category"].create({"name": "No Code"})
        self.assertEqual(category.display_name, "No Code")

    def test_export_import_compatible(self):
        """Import-compatible exports leave the code out of the category name.

        Scenario:
            1. Export the category of a product, import-compatible.
            2. Export it again, not import-compatible.
        Expected:
            - The first export has the plain category name.
            - The second export has the code in front of the name.
        """
        product = self.env["product.template"].create(
            {"name": "Product Test", "categ_id": self.category.id}
        )
        self.assertEqual(
            product.with_context(import_compat=True).export_data(["categ_id"]),
            {"datas": [["Category Test"]]},
        )
        self.assertEqual(
            product.with_context(import_compat=False).export_data(["categ_id"]),
            {"datas": [["[XYZ] Category Test"]]},
        )

    def test_search_by_code(self):
        """Categories can be found by their code.

        Scenario:
            1. Search categories by name with the category code.
            2. Search categories by display name with the category code.
        Expected:
            - Both searches find the category, although the code is not part
              of its name.
        """
        self.assertEqual(
            self.env["product.category"].name_search("XYZ"),
            [(self.category.id, "[XYZ] Category Test")],
        )
        self.assertEqual(
            self.env["product.category"].search([("display_name", "ilike", "XYZ")]),
            self.category,
        )
