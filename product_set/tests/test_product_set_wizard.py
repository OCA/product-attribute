# Copyright 2024 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import ValidationError

from .common import ProductSetCommon


class TestProductSetWizard(ProductSetCommon):
    def _create_wizard(self, product_set=None, qty=1):
        return self.env["product.set.wizard"].create(
            {
                "product_set_id": (product_set or self.product_set_1).id,
                "quantity": qty,
            }
        )

    def test_product_set_wizard_compute_lines(self):
        """Check that wizard lines update when product set changes."""
        wizard = self._create_wizard()
        self.assertEqual(wizard.product_set_id, self.product_set_1)
        self.assertEqual(wizard.product_set_line_ids, self.product_set_1.set_line_ids)
        wizard.product_set_id = self.product_set_2
        self.assertEqual(wizard.product_set_id, self.product_set_2)
        self.assertEqual(wizard.product_set_line_ids, self.product_set_2.set_line_ids)

    def test_product_set_check_partner_wizard(self):
        """Check partner validation on product set wizard.

        - No partner on the set: any wizard partner is accepted.
        - Mismatched partners: add_set() must raise ValidationError.
        - Set has a partner but wizard has none: ValidationError is raised.
        """
        wizard = self._create_wizard()
        # When a set has no partner defined, the wizard partner is irrelevant.
        wizard.partner_id = self.partner_1
        wizard.add_set()
        # When set and wizard have different partners, adding must fail.
        self.product_set_1.partner_id = self.partner_2
        with self.assertRaises(ValidationError):
            wizard.add_set()
        # When set has a partner but wizard has none, adding must fail.
        wizard.partner_id = False
        with self.assertRaises(ValidationError):
            wizard.add_set()
