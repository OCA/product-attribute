# Copyright 2024 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo_test_helper import FakeModelLoader

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestProductSetWizard(TransactionCase, FakeModelLoader):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import FakeProductSetWizard

        cls.loader.update_registry((FakeProductSetWizard,))
        cls.partner_1 = cls.env["res.partner"].create({"name": "Test Partner One"})
        cls.partner_2 = cls.env["res.partner"].create({"name": "Test Partner Two"})
        cls.product_set_1 = cls.env.ref("product_set.product_set_i5_computer")
        cls.product_set_2 = cls.env.ref("product_set.product_set_services")
        cls.wizard = cls.env["fake.product.set.wizard"].create(
            {
                "product_set_id": cls.product_set_1.id,
                "quantity": 1,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    def test_product_set_wizard_compute_lines(self):
        # Check if the wizard lines are updated when the product set changes
        self.assertTrue(self.wizard.product_set_id, self.product_set_1)
        self.assertTrue(
            self.wizard.product_set_line_ids, self.product_set_1.set_line_ids
        )
        self.wizard.product_set_id = self.product_set_2
        self.assertTrue(self.wizard.product_set_id, self.product_set_2)
        self.assertTrue(
            self.wizard.product_set_line_ids, self.product_set_2.set_line_ids
        )

    def test_product_set_check_partner_wizard(self):
        # When a set of products does not have a partner defined, even if the wizard has
        # a partner defined, this will not prevent the addition of the lines of the set.
        self.wizard.partner_id = self.partner_1
        self.wizard.add_set()
        # If the wizard and the product set have different partners defined, it will not
        # be possible to add the product set.
        self.product_set_1.partner_id = self.partner_2
        with self.assertRaises(ValidationError):
            self.wizard.add_set()
        # If a product set has a partner defined and there is no partner defined in the
        # wizard, it will not be possible to add the product set.
        self.wizard.partner_id = False
        with self.assertRaises(ValidationError):
            self.wizard.add_set()
