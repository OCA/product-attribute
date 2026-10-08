# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import ValidationError
from odoo.fields import Date

from .common import CountryRestrictionCommon


class TestCountryRestriction(CountryRestrictionCommon):
    def test_rule_lookup_and_item_names(self):
        self.assertEqual(
            self.global_item.rule_id,
            self.rule_obj._get_by_code("global"),
        )
        self.assertFalse(self.rule_obj._get_by_code("unknown"))
        self.assertEqual(
            f"{self.restriction_1.name} - {self.global_item.rule_id.name}",
            self.global_item.name,
        )
        self.assertEqual(
            f"{self.restriction_2.name} - {self.variant_item.rule_id.name} - "
            "2018-03-01 : 2018-04-30",
            self.variant_item.name,
        )

    def test_country_restriction_action(self):
        action = self.kp.action_view_country_restrictions()

        self.assertEqual(
            [
                "|",
                ("country_group_ids.country_ids", "in", [self.kp.id]),
                ("country_ids", "in", [self.kp.id]),
            ],
            action["domain"],
        )

    def test_restriction(self):
        self.assertEqual(
            self.restriction_1,
            self.au.product_country_restriction_ids,
        )

        self.assertEqual(
            self.restriction_2,
            self.kp.product_country_restriction_ids,
        )
        self.assertEqual(
            1,
            self.kp.product_country_restriction_count,
        )

        self.assertTrue(
            self.product_2._has_country_restriction(self.kp, Date.to_date("2018-03-20"))
        )
        # Test date limits
        self.assertTrue(
            self.product_2._has_country_restriction(self.kp, Date.to_date("2018-03-01"))
        )
        self.assertTrue(
            self.product_2._has_country_restriction(self.kp, Date.to_date("2018-04-30"))
        )
        self.assertFalse(
            self.product_2._has_country_restriction(self.kp, Date.to_date("2018-05-01"))
        )
        self.assertFalse(
            self.product_2._has_country_restriction(self.kp, Date.to_date("2018-02-28"))
        )
        self.assertTrue(
            self.product_2._has_country_restriction(self.au, Date.to_date("2018-03-20"))
        )

        self.assertFalse(
            self.product_2._has_country_restriction(self.be, Date.to_date("2018-03-20"))
        )

        self.assertFalse(
            self.product_3._has_country_restriction(self.kp, Date.to_date("2018-03-20"))
        )
        self.assertTrue(
            self.product_3._has_country_restriction(self.kp, Date.to_date("2018-09-20"))
        )
        # Test product 3 variant
        self.assertTrue(
            self.product_3.product_variant_ids._has_country_restriction(
                self.kp, Date.to_date("2018-09-20")
            )
        )

        self.assertFalse(
            self.product_4._has_country_restriction(self.kp, Date.to_date("2018-02-27"))
        )
        self.assertTrue(
            self.product_4._has_country_restriction(self.kp, Date.to_date("2018-08-25"))
        )

    def test_restriction_change_date(self):
        with self.assertRaises(ValidationError):
            self.restriction_2.item_ids.write(
                {"start_date": Date.to_date("2018-05-01")}
            )

    def test_restriction_inverse(self):
        # We inverse tests as strategy is 'restrict' (all products that have
        # a country rule are authorized
        self.env.company.country_restriction_strategy = "restrict"
        self.assertEqual(
            self.restriction_1,
            self.au.product_country_restriction_ids,
        )

        self.assertEqual(
            self.restriction_2,
            self.kp.product_country_restriction_ids,
        )
        self.assertEqual(
            1,
            self.kp.product_country_restriction_count,
        )

        self.assertFalse(
            self.product_2._has_country_restriction(self.kp, Date.to_date("2018-03-20"))
        )
        self.assertFalse(
            self.product_2._has_country_restriction(self.au, Date.to_date("2018-03-20"))
        )

        self.assertTrue(
            self.product_2._has_country_restriction(self.be, Date.to_date("2018-03-20"))
        )

        self.assertTrue(
            self.product_3._has_country_restriction(self.kp, Date.to_date("2018-03-20"))
        )
        self.assertFalse(
            self.product_3._has_country_restriction(self.kp, Date.to_date("2018-09-20"))
        )

        self.assertTrue(
            self.product_4._has_country_restriction(self.kp, Date.to_date("2018-02-27"))
        )
        self.assertFalse(
            self.product_4._has_country_restriction(self.kp, Date.to_date("2018-08-25"))
        )

    def test_message(self):
        restriction_obj = self.env["product.country.restriction"]
        restrictions = self.product_2._get_country_restrictions(
            self.kp, Date.to_date("2018-03-20")
        )
        messages = restriction_obj._get_country_restriction_messages(restrictions)
        self.assertEqual(
            f"The product {self.product_2.name} has country restriction for "
            f"{self.kp.name}.(Rule : {self.variant_item.name})",
            messages,
        )
        self.env.company.country_restriction_strategy = "restrict"
        restrictions = self.product_5._get_country_restrictions(
            self.kp, Date.to_date("2018-03-20")
        )
        messages = restriction_obj._get_country_restriction_messages(restrictions)
        self.assertEqual(
            f"The product {self.product_5.name} has no rule that authorize it.",
            messages,
        )
