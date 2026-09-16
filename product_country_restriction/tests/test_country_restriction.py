# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import ValidationError
from odoo.fields import Date

from .common import CountryRestrictionCommon


class TestCountryRestriction(CountryRestrictionCommon):
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
        expected_message = (
            f"The product {self.product_2.name} has country restriction "
            f"for {self.kp.name}.(Rule : {self.variant_item.name})"
        )
        self.assertEqual(
            expected_message,
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

    def test_sale_order_line_country_restriction_warning(self):
        self.partner.country_id = self.kp
        order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
                "date_order": Date.to_date("2018-03-20"),
            }
        )
        line = self.env["sale.order.line"].new(
            {
                "order_id": order.id,
                "product_id": self.product_2.id,
            }
        )
        res = line._onchange_product_id_warning()
        self.assertEqual("Country Restriction", res["warning"]["title"])
        self.assertIn(self.product_2.name, res["warning"]["message"])
        self.assertIn(self.kp.name, res["warning"]["message"])
