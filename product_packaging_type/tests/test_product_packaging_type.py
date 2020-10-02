# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase
from odoo.exceptions import ValidationError


class TestProductPackagingType(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductPackagingType, cls).setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.ProductPackagingType = cls.env["product.packaging.type"]
        cls.product_packaging_type_default = cls.env.ref(
            "product_packaging_type.product_packaging_type_default"
        )

    def test_00(self):
        """
        Data:
            A default packaging type
        Test case:
            Create a new default type
        Expected result:
            Validation Error
        """
        vals = {
            "name": "Box",
            "code": "ABC",
            "sequence": 0,
            "is_default": True,
        }
        with self.assertRaises(ValidationError), self.env.cr.savepoint():
            self.ProductPackagingType.create(vals)
        vals["is_default"] = False
        self.assertTrue(self.ProductPackagingType.create(vals))

    def test_01(self):
        """
        Data:
            A default packaging type
        Test case:
            Set as non default
        Expected result:
            Validation Error
        """
        with self.assertRaises(ValidationError), self.env.cr.savepoint():
            self.product_packaging_type_default.is_default = False
