# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductSupplierInfoPackaging(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Packaging = cls.env["product.packaging"]
        cls.Partner = cls.env["res.partner"]
        cls.SupplierInfo = cls.env["product.supplierinfo"]
        cls.product_chair = cls.env.ref("product.product_delivery_01")
        cls.product_lamp = cls.env.ref("product.product_delivery_02")

        cls.supplier = cls.Partner.create(
            {
                "name": "Supplier",
            }
        )

        cls.packaging_chair = cls.Packaging.create(
            {
                "product_id": cls.product_chair.id,
                "name": "Pallet of 10 chair",
                "qty": 10,
            }
        )

        cls.packaging_lamp = cls.Packaging.create(
            {
                "product_id": cls.product_lamp.id,
                "name": "Box of 5 lamp",
                "qty": 5,
            }
        )

        cls.supplier_info_chair = cls.SupplierInfo.create(
            {
                "product_id": cls.product_chair.id,
                "packaging_id": cls.packaging_chair.id,
                "partner_id": cls.supplier.id,
            }
        )

    def test_supplier_info_packaging_qty(self):
        info = self.supplier_info_chair
        info.packaging_min_qty = 2
        self.assertEqual(info.min_qty, 20)
        info.min_qty = 50
        self.assertEqual(info.packaging_min_qty, 5)

    def test_supplier_info_packaging_product(self):
        info = self.supplier_info_chair
        with self.assertRaises(ValidationError) as exc, self.env.cr.savepoint():
            info.packaging_id = self.packaging_lamp
        self.assertIn("Selected packaging", exc.exception.args[0])

    def test_supplier_info_packaging_domain(self):
        info = self.supplier_info_chair
        product = self.product_chair

        self.assertEqual(
            info.packaging_id_domain,
            [
                ("purchase", "=", True),
                "|",
                ("company_id", "=", self.env.user.company_id.id),
                ("company_id", "=", False),
                ("product_id", "=", product.id),
            ],
        )

    def test_supplier_info_packaging_price(self):
        info = self.supplier_info_chair
        info.price = 10
        self.assertEqual(info.packaging_price, 100)
        info.packaging_price = 80
        self.assertEqual(info.price, 8)
