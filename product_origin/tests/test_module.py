# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country_us = cls.env.ref("base.us")
        cls.state_tarapaca = cls.env.ref("base.state_cl_01")

    def test_product_product(self):
        self._test_compute_and_constrains(self.env["product.product"])

    def test_product_template(self):
        self._test_compute_and_constrains(self.env["product.template"])

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
