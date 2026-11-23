# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from odoo import fields
from odoo.exceptions import UserError

from odoo.addons.base.tests.common import BaseCommon


class TestProductPricelistRevision(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist_obj = cls.env["product.pricelist"]
        cls.pricelist_item_obj = cls.env["product.pricelist.item"]
        cls.product_category_obj = cls.env["product.category"]
        cls.product_template_obj = cls.env["product.template"]
        cls.product_product_obj = cls.env["product.product"]
        # Create a price list, a product category, a product template and
        # a product variant
        cls.pricelist = cls.pricelist_obj.create(
            {"name": "Pricelist", "item_ids": False}
        )
        cls.product_category = cls.product_category_obj.create(
            {"name": "Product Category"}
        )
        cls.product_template = cls.product_template_obj.create(
            {"name": "Product Template", "categ_id": cls.product_category.id}
        )
        cls.product_product = cls.product_product_obj.create(
            {"name": "Product Variant", "categ_id": cls.product_category.id}
        )
        # Create pricelist items
        cls.pricelist_item_global = cls.pricelist_item_obj.create(
            {
                "pricelist_id": cls.pricelist.id,
                "compute_price": "formula",
                "price_discount": 15,
            }
        )
        cls.pricelist_item_product_category = cls.pricelist_item_obj.create(
            {
                "pricelist_id": cls.pricelist.id,
                "applied_on": "2_product_category",
                "categ_id": cls.product_category.id,
                "compute_price": "formula",
                "price_discount": 10,
            }
        )
        cls.pricelist_item_product_template = cls.pricelist_item_obj.create(
            {
                "pricelist_id": cls.pricelist.id,
                "applied_on": "1_product",
                "product_tmpl_id": cls.product_template.id,
                "compute_price": "percentage",
                "percent_price": 5,
            }
        )
        cls.pricelist_item_product_product = cls.pricelist_item_obj.create(
            {
                "pricelist_id": cls.pricelist.id,
                "applied_on": "0_product_variant",
                "product_id": cls.product_product.id,
                "compute_price": "fixed",
                "fixed_price": 100,
            }
        )

    def test_search_name(self):
        item_obj = self.pricelist_item_obj
        result = item_obj.search([])
        expected = self.pricelist_item_product_category
        expected |= self.pricelist_item_product_template
        expected |= self.pricelist_item_product_product
        for exp in expected:
            self.assertIn(exp, result)
        result = item_obj.search([("categ_id.name", "ilike", "product category")])
        self.assertEqual(result, self.pricelist_item_product_category)
        result = item_obj.search(
            [("product_tmpl_id.name", "ilike", "product template")]
        )
        self.assertEqual(result, self.pricelist_item_product_template)
        result = item_obj.search([("product_id.name", "ilike", "product variant")])
        self.assertEqual(result, self.pricelist_item_product_product)
        result = item_obj.search([("pricelist_id.name", "ilike", "all")])
        self.assertEqual(len(result), 0)

    def test_wizard_action_apply_and_compute_variation_percent(self):
        wizard_obj = self.env["product.pricelist.item.duplicate.wizard"]
        # Before duplicate there are 4 items
        self.assertEqual(len(self.pricelist.item_ids), 4)
        items_before_wizard = self.pricelist.item_ids
        # Create wizard from pricelist_item_product_product and aply
        active_ids = self.pricelist_item_product_product.ids
        wizard = wizard_obj.with_context(active_ids=active_ids).create(
            {
                "date_start": datetime.now(),
                "date_end": datetime.now() + timedelta(hours=1),
                "variation_percent": 50,
            }
        )
        wizard.action_apply()
        # There will be one more item in self.pricelist
        self.assertEqual(len(self.pricelist.item_ids), 5)
        new_item = self.pricelist.item_ids - items_before_wizard
        self.assertEqual(new_item.previous_item_id.id, active_ids[0])
        self.assertEqual(new_item.previous_price, 100)
        self.assertEqual(new_item.fixed_price, 150)
        self.assertEqual(new_item.variation_percent, 50)

    def _pricelist_wizard(self, pricelist, **vals):
        vals.setdefault("date_start", fields.Datetime.now())
        vals.setdefault("variation_percent", 10)
        return (
            self.env["product.pricelist.item.duplicate.wizard"]
            .with_context(active_model="product.pricelist", active_id=pricelist.id)
            .create(vals)
        )

    def test_wizard_default_pricelist_from_context(self):
        wizard = self._pricelist_wizard(self.pricelist)
        self.assertEqual(wizard.pricelist_id, self.pricelist)

    def test_wizard_revise_whole_pricelist(self):
        other_category = self.product_category_obj.create({"name": "Other"})
        other_product = self.product_product_obj.create(
            {"name": "Other Variant", "categ_id": other_category.id}
        )
        second_fixed = self.pricelist_item_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "0_product_variant",
                "product_id": other_product.id,
                "compute_price": "fixed",
                "fixed_price": 40,
            }
        )
        start = fields.Datetime.now()
        expired = self.pricelist_item_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "0_product_variant",
                "product_id": other_product.id,
                "compute_price": "fixed",
                "fixed_price": 30,
                "date_end": start - timedelta(days=10),
            }
        )
        items_before = self.pricelist.item_ids
        self._pricelist_wizard(self.pricelist, date_start=start).action_apply()
        new_items = self.pricelist.item_ids - items_before
        # Only the two still valid fixed price items are revised
        self.assertEqual(len(new_items), 2)
        self.assertEqual(
            new_items.previous_item_id,
            self.pricelist_item_product_product | second_fixed,
        )
        for got, expected in zip(
            sorted(new_items.mapped("fixed_price")), [44.0, 110.0], strict=True
        ):
            self.assertAlmostEqual(got, expected)
        for item in self.pricelist_item_product_product | second_fixed:
            self.assertEqual(item.date_end, start - timedelta(seconds=1))
        self.assertEqual(expired.date_end, start - timedelta(days=10))
        self.assertFalse(self.pricelist_item_global.date_end)

    def test_wizard_revise_pricelist_category_filter(self):
        other_category = self.product_category_obj.create({"name": "Other"})
        other_product = self.product_product_obj.create(
            {"name": "Other Variant", "categ_id": other_category.id}
        )
        other_item = self.pricelist_item_obj.create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "0_product_variant",
                "product_id": other_product.id,
                "compute_price": "fixed",
                "fixed_price": 40,
            }
        )
        items_before = self.pricelist.item_ids
        self._pricelist_wizard(
            self.pricelist, categ_id=self.product_category.id
        ).action_apply()
        new_items = self.pricelist.item_ids - items_before
        self.assertEqual(
            new_items.previous_item_id, self.pricelist_item_product_product
        )
        self.assertFalse(other_item.date_end)

    def test_wizard_selected_items_skips_non_fixed(self):
        wizard = (
            self.env["product.pricelist.item.duplicate.wizard"]
            .with_context(
                active_ids=(
                    self.pricelist_item_product_product
                    | self.pricelist_item_product_template
                ).ids
            )
            .create({"date_start": datetime.now(), "variation_percent": 10})
        )
        items_before = self.pricelist.item_ids
        action = wizard.action_apply()
        new_items = self.pricelist.item_ids - items_before
        self.assertEqual(
            new_items.previous_item_id, self.pricelist_item_product_product
        )
        self.assertEqual(action["tag"], "display_notification")
        self.assertEqual(
            action["params"]["next"]["domain"], [("id", "in", new_items.ids)]
        )
        self.assertFalse(self.pricelist_item_product_template.date_end)

    def test_wizard_nothing_to_revise(self):
        empty = self.pricelist_obj.create({"name": "Empty", "item_ids": False})
        with self.assertRaises(UserError):
            self._pricelist_wizard(empty).action_apply()
