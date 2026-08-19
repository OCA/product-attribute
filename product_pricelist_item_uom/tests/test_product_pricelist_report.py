# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Command
from odoo.tests.common import tagged

from .common import TestPricelistItemUomCommon


@tagged("post_install", "-at_install")
class TestProductPricelistReport(TestPricelistItemUomCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.report = cls.env["report.product.report_pricelist"]

    def _get_report_products(self, records):
        return self.report._get_report_data(
            {
                "pricelist_id": self.pricelist.id,
                "active_model": records._name,
                "active_ids": records.ids,
                "quantities": [1],
            }
        )["products"]

    def test_report_one_row_per_packaging(self):
        self._create_rule(fixed_price=10.0, uom_id=self.uom_unit.id)
        self._create_rule(fixed_price=20.0, uom_id=self.uom_pack_6.id)

        product_data = self._get_report_products(self.product_tmpl)[0]

        self.assertEqual(
            {uom["id"] for uom in product_data["uoms"]},
            {self.uom_unit.id, self.uom_pack_6.id},
        )
        self.assertEqual(product_data["price"][self.uom_unit.id][1], 10.0)
        # Fixed prices are expressed in the product base UoM, so the packaging
        # row shows the price of the six units of the packaging-specific rule.
        self.assertEqual(product_data["price"][self.uom_pack_6.id][1], 120.0)

    def test_report_single_row_without_packaging_rule(self):
        """Without a packaging rule, the report keeps a single row."""
        self._create_rule(fixed_price=10.0)

        product_data = self._get_report_products(self.product_tmpl)[0]

        self.assertEqual(
            [uom["id"] for uom in product_data["uoms"]], [self.uom_unit.id]
        )
        self.assertEqual(product_data["price"][self.uom_unit.id][1], 10.0)

    def test_report_renders_with_variants(self):
        """The rendered report has one row per variant and per packaging."""
        attribute = self.env["product.attribute"].create(
            {
                "name": "Test Colour",
                "value_ids": [
                    Command.create({"name": "Test Red"}),
                    Command.create({"name": "Test Blue"}),
                ],
            }
        )
        self.product_tmpl.attribute_line_ids = [
            Command.create(
                {
                    "attribute_id": attribute.id,
                    "value_ids": [Command.set(attribute.value_ids.ids)],
                }
            )
        ]
        self._create_rule(fixed_price=20.0, uom_id=self.uom_pack_6.id)

        render_values = self.report._get_report_data(
            {
                "pricelist_id": self.pricelist.id,
                "active_model": "product.template",
                "active_ids": self.product_tmpl.ids,
                "quantities": [1],
            }
        )
        product_data = render_values["products"][0]

        self.assertEqual(len(product_data["variants"]), 2)
        for variant_data in product_data["variants"]:
            self.assertEqual(
                {uom["id"] for uom in variant_data["uoms"]},
                {self.uom_unit.id, self.uom_pack_6.id},
            )

        html = self.env["ir.qweb"]._render(
            "product.report_pricelist_page", render_values
        )
        self.assertIn("Test Red", str(html))
