# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import Command

from odoo.addons.product_packaging_template.tests.test_product_packaging_template import (  # noqa: E501
    TestProductPackagingTemplate as BaseTestProductPackagingTemplate,
)


class TestProductPackagingTemplate(BaseTestProductPackagingTemplate):
    def test_purchase_on_packaging_template_default_value(self):
        self.template.packaging_tmpl_ids = [
            Command.create({"name": "Box of 10", "qty": 10})
        ]
        self.assertTrue(self.variant_1.packaging_ids.purchase)
        self.assertTrue(self.variant_2.packaging_ids.purchase)
        self.template.packaging_tmpl_ids.write({"purchase": False})
        self.assertFalse(self.variant_1.packaging_ids.purchase)
        self.assertFalse(self.variant_2.packaging_ids.purchase)
        self.template.packaging_tmpl_ids.unlink()
        self.template.packaging_tmpl_ids = [
            Command.create({"name": "Box of 20", "qty": 20, "purchase": False})
        ]
        self.assertFalse(self.variant_1.packaging_ids.purchase)
        self.assertFalse(self.variant_2.packaging_ids.purchase)
