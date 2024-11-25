# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.tests import tagged

from odoo.addons.product_pricelist_direct_print.tests.common import Common


@tagged("post_install", "-at_install")
class TestPricelistExportWebsiteSale(Common):
    def _get_wiz(self):
        return self.wiz_obj.with_context(
            active_model="product.pricelist", active_id=self.pricelist.id
        ).create({})

    def test_xlsx_header(self):
        wiz = self._get_wiz()
        report = self.env["report.product_pricelist_direct_print_xlsx.report"]
        # When show_public_category is False, `Public Category` isn't in the
        # header
        wiz.show_public_category = False
        self.assertNotIn("Public Category", report._get_header_values(wiz))
        # When show_public_category is True, `Public Category` is in the header
        wiz.show_public_category = True
        self.assertIn("Public Category", report._get_header_values(wiz))

    def test_xlsx_values(self):
        wiz = self._get_wiz()
        public_category = self.env["product.public.category"].create(
            {"name": "public category"}
        )
        # For some reason, this is required to get it populated in order to have
        # the display name right
        public_category._compute_parents_and_self()
        # import pdb; pdb.set_trace()
        product = self.env["product.product"].create(
            {
                "name": "test product",
                "public_categ_ids": [(6, 0, public_category.ids)],
            }
        )
        report = self.env["report.product_pricelist_direct_print_xlsx.report"]
        # When show_public_category is False, `Public Category` isn't in the
        # header
        wiz.show_public_category = False
        values = [value for value, __ in report._get_row_values(wiz, product, {})]
        self.assertNotIn("selleable stuff", values)
        # When show_public_category is True, `Public Category` is there
        wiz.show_public_category = True
        # This is the place where we expect to find the category value
        index = report._get_header_values(wiz).index("Public Category")
        # If a category is set on the product, we should have its name in the values
        values = [value for value, __ in report._get_row_values(wiz, product, {})]
        self.assertEqual(values[index], "public category")
        # If no category is set on the product, we should have an empty string instead
        product.public_categ_ids = False
        values = [value for value, __ in report._get_row_values(wiz, product, {})]
        self.assertEqual(values[index], "")
