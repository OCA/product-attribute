# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests import Form, TransactionCase


class TestProductPricelistItem(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist = cls.env["product.pricelist"].create({"name": "Test"})
        cls.product = cls.env["product.template"].create({"name": "Test Product"})
        cls.tag = cls.env["product.tag"].create({"name": "Test Tag"})

    def _new_item(self):
        return Form(
            self.env["product.pricelist.item"].with_context(
                default_pricelist_id=self.pricelist.id
            )
        )

    def test_item_on_product(self):
        with self._new_item() as item_form:
            item_form.display_applied_on = "1_product"
            item_form.product_tmpl_id = self.product
        item = item_form.record
        self.assertEqual(item.applied_on, "1_product")
        self.assertEqual(item.product_tmpl_id, self.product)
        self.assertEqual(item.name, self.product.display_name)

    def test_item_on_tag(self):
        with self._new_item() as item_form:
            item_form.display_applied_on = "product_tag"
            item_form.product_tag_id = self.tag
            item_form.display_applied_on = "1_product"
            self.assertEqual(item_form.applied_on, "3_global")
            item_form.display_applied_on = "product_tag"
        item = item_form.record
        self.assertEqual(item.applied_on, "product_tag")
        self.assertEqual(item.product_tag_id, self.tag)

    def test_write_applied_on_tag(self):
        item = self.env["product.pricelist.item"].create(
            {"pricelist_id": self.pricelist.id, "product_tmpl_id": self.product.id}
        )
        item.write({"applied_on": "product_tag", "product_tag_id": self.tag.id})
        self.assertFalse(item.product_tmpl_id)
        self.assertEqual(item.name, f"Tag: {self.tag.display_name}")

    def test_tag_required(self):
        with self.assertRaises(ValidationError):
            self.env["product.pricelist.item"].create(
                {"pricelist_id": self.pricelist.id, "applied_on": "product_tag"}
            )

    def test_price_product_with_several_tags(self):
        other_tag = self.env["product.tag"].create({"name": "Other Tag"})
        self.product.product_tag_ids = self.tag | other_tag
        untagged = self.env["product.template"].create(
            {"name": "Untagged", "list_price": 100.0}
        )
        self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "product_tag_id": self.tag.id,
                "compute_price": "fixed",
                "fixed_price": 42.0,
            }
        )
        self.assertEqual(self.pricelist._get_product_price(self.product, 1.0), 42.0)
        self.assertEqual(
            self.pricelist._get_product_price(self.product.product_variant_id, 1.0),
            42.0,
        )
        self.assertEqual(self.pricelist._get_product_price(untagged, 1.0), 100.0)
