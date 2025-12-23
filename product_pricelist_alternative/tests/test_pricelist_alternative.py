# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError
from odoo.fields import Command
from odoo.tests import tagged

from .common import CommonProductPricelistAlternative


@tagged("post_install", "-at_install")
class TestPricelistAlternative(CommonProductPricelistAlternative):
    def test_is_alternative_to_pricelist_count(self):
        """Test the alternative pricelist usage count is correctly computed."""
        self.assertEqual(
            self.alternative_pricelist_01.is_alternative_to_pricelist_count, 2
        )
        self.assertEqual(
            self.alternative_pricelist_02.is_alternative_to_pricelist_count, 1
        )

    def test_action_view_is_alternative_to_pricelist(self):
        """Test the action opens pricelists using this alternative pricelist."""
        action = self.alternative_pricelist_01.action_view_is_alternative_to_pricelist()
        self.assertEqual(action["view_mode"], "list,form")
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

    def test_product_price_uses_lower_alternative_pricelist(self):
        """Test the product price uses the lower alternative pricelist price."""

        # Best price on alternative pricelist01
        result = self.pricelist01._compute_price_rule(
            self.usb_adapter, 1.0, uom=self.usb_adapter.uom_id
        )
        self.assertEqual(result[self.usb_adapter.id][0], 70.0)
        self.assertEqual(
            result[self.usb_adapter.id][1], self.alternative_pricelist_01.item_ids[0].id
        )
        # Best price on pricelist02
        result = self.pricelist02._compute_price_rule(
            self.usb_adapter, 1.0, uom=self.usb_adapter.uom_id
        )
        self.assertEqual(result[self.usb_adapter.id][0], 60.0)
        self.assertEqual(
            result[self.usb_adapter.id][1], self.pricelist02.item_ids[0].id
        )

    def test_product_price_formula_based_on_other_price(self):
        """Test base pricelist formulas do not apply alternatives.

        The chained pricelist must use the regular price from its base
        pricelist, not the base pricelist's lower alternative price.
        """
        self.assertEqual(self.pricelist03._get_product_price(self.usb_adapter, 1.0), 95)

    def test_configurable_template_combination_uses_variant_alternative_price(self):
        """Test selected variants use their alternative promotion price.

        The sale configurator prices a product template with a selected
        combination in context before creating the final sale order line.
        """

        product = self.configurable_product_template.with_context(
            **self.configurable_product_template._get_product_price_context(
                self.yellow_combination
            )
        )
        result = self.configurable_pricelist._compute_price_rule(
            product, 1.0, uom=product.uom_id
        )
        rule = self.configurable_pricelist._get_product_rule(self.yellow_gloves, 1.0)
        self.assertEqual(
            self.configurable_pricelist.currency_id.compare_amounts(
                result[product.id][0], 41.5
            ),
            0,
        )
        self.assertEqual(
            result[product.id][1],
            self.alternative_promotion_pricelist.item_ids.id,
        )
        self.assertEqual(rule, self.alternative_promotion_pricelist.item_ids.id)

    def test_variant_alternative_lower_price_uses_raw_unit_price(self):
        """Test sub-cent alternative prices are not rounded before comparison."""
        alternative_pricelist = self.env["product.pricelist"].create(
            {
                "name": "Alternative sub-cent promotion pricelist",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": self.yellow_gloves.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 0.0123,
                        }
                    ),
                ],
            }
        )
        pricelist = self.env["product.pricelist"].create(
            {
                "name": "Variant sub-cent client pricelist",
                "item_ids": [
                    Command.create(
                        {
                            "compute_price": "fixed",
                            "product_id": self.yellow_gloves.id,
                            "applied_on": "0_product_variant",
                            "fixed_price": 0.0131,
                        }
                    ),
                ],
                "alternative_pricelist_ids": [
                    Command.link(alternative_pricelist.id),
                ],
            }
        )

        result = pricelist._compute_price_rule(
            self.yellow_gloves, 200.0, uom=self.yellow_gloves.uom_id
        )
        rule = pricelist._get_product_rule(self.yellow_gloves, 200.0)

        self.assertEqual(result[self.yellow_gloves.id][0], 0.0123)
        self.assertEqual(
            result[self.yellow_gloves.id][1],
            alternative_pricelist.item_ids.id,
        )
        self.assertEqual(rule, alternative_pricelist.item_ids.id)

    def test_product_price_ignores_alternative_pricelist(self):
        """Test the product price ignores alternative pricelists by policy."""

        # Set the pricelist items policy to ignore alternative pricelist
        self.pricelist01.item_ids.write({"alternative_pricelist_policy": "ignore"})
        self.pricelist02.item_ids.write({"alternative_pricelist_policy": "ignore"})

        # We won't consider the alternative pricelist
        self.assertEqual(self.pricelist01._get_product_price(self.usb_adapter, 1.0), 95)
        self.assertEqual(self.pricelist02._get_product_price(self.usb_adapter, 1.0), 60)

        result = self.pricelist01._compute_price_rule(
            self.usb_adapter, 1.0, uom=self.usb_adapter.uom_id
        )
        self.assertEqual(result[self.usb_adapter.id][0], 95.0)
        self.assertEqual(
            result[self.usb_adapter.id][1], self.pricelist01.item_ids[1].id
        )
        result = self.pricelist02._compute_price_rule(
            self.usb_adapter, 1.0, uom=self.usb_adapter.uom_id
        )
        self.assertEqual(result[self.usb_adapter.id][0], 60.0)
        self.assertEqual(
            result[self.usb_adapter.id][1], self.pricelist02.item_ids[0].id
        )

    def test_skip_alternative_pricelist(self):
        """Test product price computation can skip alternative pricelists."""
        self.assertEqual(self.pricelist01._get_product_price(self.usb_adapter, 1.0), 70)
        # Set the context to skip alternative pricelist
        self.assertEqual(
            self.pricelist01.with_context(
                skip_alternative_pricelist=True
            )._get_product_price(self.usb_adapter, 1.0),
            95,
        )

    def test_check_pricelist_alternative_items_based_on_other_pricelist(self):
        """Test alternative pricelists cannot use formulas based on pricelists."""
        msg = (
            "Formulas based on another pricelist "
            "are not allowed on alternative pricelists."
        )
        with self.assertRaisesRegex(ValidationError, msg):
            self.alternative_pricelist_01.item_ids.write(
                {
                    "compute_price": "formula",
                    "base": "pricelist",
                    "base_pricelist_id": self.alternative_pricelist_02.id,
                }
            )
