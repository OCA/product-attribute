# Copyright 2021 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestProductStateActive(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.state_draft = cls.env.ref("product_state.product_state_draft")
        cls.state_sellable = cls.env.ref("product_state.product_state_sellable")
        cls.product_1 = cls.env.ref("product.product_product_4_product_template")

    def test_constraint(self):
        """
        Try to set both options True
        """
        with self.assertRaises(ValidationError):
            self.state_draft.write(
                {
                    "activate_product": True,
                    "deactivate_product": True,
                }
            )

    def test_deactivate_from_state_id(self):
        """
        Change the state that deactivate a product
        Check if deactivated
        Change the state that activate a product
        Check if activated
        """
        self.state_draft.deactivate_product = True
        self.state_sellable.activate_product = True
        self.product_1.product_state_id = self.state_draft
        self.assertFalse(self.product_1.active)
        self.product_1.product_state_id = self.state_sellable
        self.assertTrue(self.product_1.active)

    def test_deactivate_from_state(self):
        """
        Change the state that deactivate a product
        Check if deactivated
        Change the state that activate a product
        Check if activated
        """
        self.state_draft.deactivate_product = True
        self.state_sellable.activate_product = True
        self.product_1.state = self.state_draft.code
        self.assertFalse(self.product_1.active)
        self.product_1.state = self.state_sellable.code
        self.assertTrue(self.product_1.active)
