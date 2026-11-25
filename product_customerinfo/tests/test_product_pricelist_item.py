# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from unittest.mock import patch

from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.product.models.product_pricelist_item import (
    ProductPricelistItem as CoreItem,
)
from odoo.addons.product_customerinfo.models.product_pricelist_item import (
    ProductPricelistItem as CustomerinfoItem,
)


class TestProductPricelistItem(BaseCommon):
    _test_user_groups = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist = cls.env["product.pricelist"].create({"name": "Test"})
        cls.other_pricelist = cls.env["product.pricelist"].create({"name": "Other"})

    def _discount_item(self, **vals):
        return self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist.id,
                "compute_price": "discount",
                "price_discount": 10,
                **vals,
            }
        )

    def test_label_names_the_customer_prices(self):
        item = self._discount_item(base="partner")
        self.assertIn("customer prices", item.price)
        self.assertNotIn("sales price", item.price)

    def test_label_of_other_bases_is_untouched(self):
        item = self._discount_item(base="list_price")
        self.assertIn("sales price", item.price)

    def test_partner_base_clears_the_base_pricelist(self):
        item = self._discount_item(
            base="pricelist", base_pricelist_id=self.other_pricelist.id
        )
        with Form(item) as form:
            form.base = "partner"
            self.assertFalse(form.base_pricelist_id)
        self.assertEqual(item.base, "partner")
        self.assertFalse(item.base_pricelist_id)

    def test_sales_price_base_clears_the_base_pricelist(self):
        item = self._discount_item(
            base="pricelist", base_pricelist_id=self.other_pricelist.id
        )
        with Form(item) as form:
            form.base = "list_price"
            self.assertFalse(form.base_pricelist_id)
        self.assertEqual(item.base, "list_price")
        self.assertFalse(item.base_pricelist_id)

    def test_partner_base_survives_the_pricelist_onchange(self):
        item = self._discount_item(base="partner")
        item._onchange_base_pricelist_id()
        self.assertEqual(item.base, "partner")

    def test_picking_a_pricelist_sets_the_pricelist_base(self):
        item = self._discount_item(base="list_price")
        item.base_pricelist_id = self.other_pricelist
        item._onchange_base_pricelist_id()
        self.assertEqual(item.base, "pricelist")

    def test_other_bases_keep_the_base_pricelist(self):
        item = self._discount_item(
            base="pricelist", base_pricelist_id=self.other_pricelist.id
        )
        item._onchange_base_clear_pricelist()
        self.assertEqual(item.base_pricelist_id, self.other_pricelist)

    def _show_discount(self, item, feature_enabled=True, core_result=False):
        # `sale` defines both methods, and it is not a dependency of the module
        with (
            patch.object(
                CoreItem, "_show_discount", create=True, return_value=core_result
            ),
            patch.object(
                type(item),
                "_is_discount_feature_enabled",
                create=True,
                return_value=feature_enabled,
            ),
        ):
            return CustomerinfoItem._show_discount(item)

    def test_show_discount_of_customer_prices(self):
        for compute_price in ("discount", "markup"):
            item = self._discount_item(base="partner", compute_price=compute_price)
            self.assertTrue(self._show_discount(item))

    def test_show_discount_needs_the_discount_feature(self):
        item = self._discount_item(base="partner")
        self.assertFalse(self._show_discount(item, feature_enabled=False))

    def test_show_discount_of_other_bases_is_untouched(self):
        item = self._discount_item(base="list_price")
        self.assertFalse(self._show_discount(item))
        self.assertTrue(self._show_discount(item, core_result=True))

    def test_show_discount_of_no_rule(self):
        item = self.env["product.pricelist.item"]
        self.assertFalse(self._show_discount(item))
