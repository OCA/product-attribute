# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError

from odoo.addons.base.tests.common import BaseCommon


class TestModule(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country_us = cls.env.ref("base.us")
        cls.state_tarapaca = cls.env.ref("base.state_cl_01")
        cls.state_us = cls.env.ref("base.state_us_1")
        cls.country_chile = cls.env.ref("base.cl")

    def test_product_product(self):
        self._test_compute_and_constrains(self.env["product.product"])
        self._test_onchange_methods(self.env["product.product"])

    def test_product_template(self):
        self._test_compute_and_constrains(self.env["product.template"])
        self._test_onchange_methods(self.env["product.template"])

    def _test_compute_and_constrains(self, model):
        # Set state should set country
        product = model.create({"name": "Test Name"})
        self.assertEqual(product.state_id_domain, [])

        product.country_id = self.country_us
        self.assertEqual(
            product.state_id_domain, [("country_id", "=", self.country_us.id)]
        )

        with self.assertRaises(ValidationError):
            product.state_id = self.state_tarapaca

    def _test_onchange_methods(self, model):
        # Test 1: onchange_country_id - When country changes,
        # mismatched state is cleared
        product = model.create({"name": "Test Onchange"})

        # Set state first
        product.state_id = self.state_us
        # Set matching country
        product.country_id = self.country_us

        # Create a new product with a temporary state/country combination
        # that we'll modify through onchange
        product_for_onchange = model.new(
            {
                "name": "Test Onchange Product",
                "state_id": self.state_us.id,
                "country_id": self.country_us.id,
            }
        )

        # Verify initial state
        self.assertEqual(product_for_onchange.state_id.id, self.state_us.id)
        self.assertEqual(product_for_onchange.country_id.id, self.country_us.id)

        # Change country and trigger onchange
        product_for_onchange.country_id = self.country_chile
        product_for_onchange.onchange_country_id()

        # State should be cleared because it doesn't match country
        self.assertFalse(product_for_onchange.state_id)

        # Test 2: onchange_state_id - When state changes, country should update
        product_for_state_change = model.new(
            {
                "name": "Test Onchange State",
            }
        )

        # Initially no country
        self.assertFalse(product_for_state_change.country_id)

        # Set state and trigger onchange
        product_for_state_change.state_id = self.state_us
        product_for_state_change.onchange_state_id()

        # Country should be set to match state's country
        self.assertEqual(product_for_state_change.country_id.id, self.country_us.id)
