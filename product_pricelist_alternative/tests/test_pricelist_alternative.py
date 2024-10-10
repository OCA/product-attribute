# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError
from odoo.tests import common, tagged

from .common import CommonProductPricelistAlternative


@tagged("post_install", "-at_install")
class TestPricelistAlternative(
    CommonProductPricelistAlternative, common.TransactionCase
):
    def test_is_alternative_to_pricelist_count(self):
        """Test that the is_alternative_to_pricelist_count is correctly computed"""

        self.assertEqual(
            self.alternative_pricelist_01.is_alternative_to_pricelist_count, 2
        )
        self.assertEqual(
            self.alternative_pricelist_02.is_alternative_to_pricelist_count, 1
        )

    def test_action_view_is_alternative_to_pricelist(self):
        action = self.alternative_pricelist_01.action_view_is_alternative_to_pricelist()
        self.assertEqual(action["view_mode"], "tree,form")
        self.assertEqual(
            action["domain"][0][2],
            self.alternative_pricelist_01.is_alternative_to_pricelist_ids.ids,
        )

        action = self.alternative_pricelist_02.action_view_is_alternative_to_pricelist()
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(
            action["domain"][0][2],
            self.alternative_pricelist_02.is_alternative_to_pricelist_ids.ids,
        )

    def test_product_price_considering_alternative_pricelist_with_lower_price(self):
        """Test that the product price is computed considering the alternative
        pricelist with the lower price"""

        # Best price on alternative pricelist01
        result = self.pricelist01._compute_price_rule(
            self.usb_adapter, 1.0, self.usb_adapter.uom_id
        )
        self.assertEqual(result[self.usb_adapter.id][0], 70.0)
        self.assertEqual(
            result[self.usb_adapter.id][1], self.alternative_pricelist_01.item_ids[0].id
        )
        # Best price on pricelist02
        result = self.pricelist02._compute_price_rule(
            self.usb_adapter, 1.0, self.usb_adapter.uom_id
        )
        self.assertEqual(result[self.usb_adapter.id][0], 60.0)
        self.assertEqual(
            result[self.usb_adapter.id][1], self.pricelist02.item_ids[0].id
        )

    def test_product_price_ignore_alternative_pricelist(self):
        """Test that the product price ignore alternative pricelist"""

        # Set the pricelist items policy to ignore alternative pricelist
        self.pricelist01.item_ids.write({"alternative_pricelist_policy": "ignore"})
        self.pricelist02.item_ids.write({"alternative_pricelist_policy": "ignore"})

        # We won't consider the alternative pricelist
        self.assertEqual(self.pricelist01._get_product_price(self.usb_adapter, 1.0), 95)
        self.assertEqual(self.pricelist02._get_product_price(self.usb_adapter, 1.0), 60)

        result = self.pricelist01._compute_price_rule(
            self.usb_adapter, 1.0, self.usb_adapter.uom_id
        )
        self.assertEqual(result[self.usb_adapter.id][0], 95.0)
        self.assertEqual(
            result[self.usb_adapter.id][1], self.pricelist01.item_ids[1].id
        )
        result = self.pricelist02._compute_price_rule(
            self.usb_adapter, 1.0, self.usb_adapter.uom_id
        )
        self.assertEqual(result[self.usb_adapter.id][0], 60.0)
        self.assertEqual(
            result[self.usb_adapter.id][1], self.pricelist02.item_ids[0].id
        )

    def test_skip_alternative_pricelist(self):
        """Test product price computation with skip alternative pricelist"""
        self.assertEqual(self.pricelist01._get_product_price(self.usb_adapter, 1.0), 70)
        # Set the context to skip alternative pricelist
        self.assertEqual(
            self.pricelist01.with_context(
                skip_alternative_pricelist=True
            )._get_product_price(self.usb_adapter, 1.0),
            95,
        )

    def test_check_pricelist_alternative_items_based_on_other_pricelist(self):
        with self.assertRaises(ValidationError) as e:
            self.alternative_pricelist_01.item_ids.write(
                {
                    "compute_price": "formula",
                    "base": "pricelist",
                    "base_pricelist_id": self.alternative_pricelist_02.id,
                }
            )
        msg = "Formulas based on another pricelist are not allowed on alternative pricelists."
        self.assertIn(msg, e.exception.args[0])
