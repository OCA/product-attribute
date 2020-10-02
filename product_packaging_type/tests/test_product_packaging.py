# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import SavepointCase
from odoo.exceptions import ValidationError


class TestProductPackaging(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestProductPackaging, cls).setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.ProductPackagingType = cls.env["product.packaging.type"]
        cls.ProductPackaging = cls.env["product.packaging"]
        cls.product_packaging_type_default = cls.env.ref(
            "product_packaging_type.product_packaging_type_default"
        )
        cls.product = cls.env.ref("product.product_product_4")
        cls.product_tmpl = cls.product.product_tmpl_id
        cls.pkg_type_box = cls.ProductPackagingType.create(
            {
                "name": "Type Box",
                "code": "ABC",
                "sequence": 0,
                "is_default": False,
            }
        )

        cls.pkg_box = cls.env["product.packaging"].create(
            {
                "name": "Box",
                "product_tmpl_id": cls.product_tmpl.id,
                "packaging_type_id": cls.pkg_type_box.id,
            }
        )

    def test_00(self):
        """
        Data:
            A Box packaging with package of packaging type box
        Test case:
            Create a new packaging with the same type
        Expected result:
            Validation Error
        """
        with self.assertRaises(ValidationError), self.env.cr.savepoint():
            self.env["product.packaging"].create(
                {
                    "name": "Test Box",
                    "product_tmpl_id": self.product_tmpl.id,
                    "packaging_type_id": self.pkg_type_box.id,
                }
            )
        self.assertTrue(
            self.env["product.packaging"].create(
                {"name": "Test Box", "product_tmpl_id": self.product_tmpl.id}
            )
        )

    def test_01(self):
        """
        Data:
            A Box packaging with qty 5
            A Box 15 packaging with qty 15
            A Box 50 packaging with qty 50
            A Box 25 packaging with qty 25
        Test case:
            Read qty_per_type
        """
        for qty in (25, 50, 15, 5):
            pkg_type = self.ProductPackagingType.create(
                {
                    "name": "Type %s box" % qty,
                    "code": "ABC %s" % qty,
                    "sequence": 0,
                    "is_default": False,
                }
            )
            pkg = self.env["product.packaging"].create(
                {
                    "name": "Test Box %s" % qty,
                    "product_tmpl_id": self.product_tmpl.id,
                    "qty": qty,
                    "packaging_type_id": pkg_type.id,
                }
            )
            setattr(self, "pkg_%s" % qty, pkg)
        self.assertEqual(self.pkg_5.qty_per_type, "")
        self.assertEqual(self.pkg_15.qty_per_type, "3.0 ABC 5")
        self.assertEqual(
            self.pkg_50.qty_per_type,
            '10.0 ABC 5; 3<span style="color: red;">.333333333333</span> '
            "ABC 15; 2.0 ABC 25",
        )
        self.assertEqual(
            self.pkg_25.qty_per_type,
            '5.0 ABC 5; 1<span style="color: red;">.666666666667</span> '
            "ABC 15"
            "",
        )
