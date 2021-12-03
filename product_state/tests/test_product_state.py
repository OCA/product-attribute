# Copyright 2021 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import SavepointCase

_logger = logging.getLogger(__name__)


class TestProductState(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductState = cls.env["product.state"]
        cls.state = cls.ProductState.create({"name": "State Name", "code": "Code"})
        cls.product_obj = cls.env["product.template"]
        cls.product_1 = cls.env.ref("product.product_product_4_product_template")

    @classmethod
    def _create_product(cls, state=None):
        vals = {
            "name": "Product Test for State",
        }
        if state:
            vals.update({"product_state_id": state.id})
        cls.product = cls.product_obj.create(vals)

    def test_01_product_state(self):
        """
        Check if existing product has the default value (see init_hook)
        Check if new state has no products
        Create a product, check if it has the default state
        Create a product with state
        Check if new state has 1 product
        """
        self.assertTrue(self.product_1.product_state_id)
        self.assertFalse(
            self.state.products_count,
        )
        self._create_product()
        self.assertEqual(
            self.env.ref("product_state.product_state_sellable"),
            self.product.product_state_id,
        )
        self._create_product(self.state)
        self.assertEqual(
            self.state,
            self.product.product_state_id,
        )
        self.assertEqual(
            1,
            self.state.products_count,
        )

    def test_02_set_product_state(self):
        """
        Create product, it has default state
        Then, update the state
        It should have the existing one (Code)
        """
        self._create_product()
        self.assertEqual(
            self.env.ref("product_state.product_state_sellable"),
            self.product.product_state_id,
        )
        self.product.state = "Code"
        self.assertEqual(
            self.state,
            self.product.product_state_id,
        )

    def test_03_set_constrains_product_state(self):
        """
        Create another default state,
        It should have the existing only one default state at time
        """

        with self.assertRaises(ValidationError) as cm:
            self.env["product.state"].create(
                {"name": "Default State 2", "code": "df2", "default": True}
            )
            wn_expect = cm.exception.args[0]
            self.assertEqual("There should be only one default state", wn_expect)

    def test_04_invalid_state(self):
        self._create_product()
        with self.assertRaises(UserError):
            self.product.state = "new_code"
