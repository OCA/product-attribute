# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.base.tests.common import BaseCommon


class TestProductPackagingArchive(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create({"name": "Test Product"})
        # In Odoo 19.0, product.uom (packaging) uses 'barcode' and 'uom_id'
        cls.uom = cls.env.ref("uom.product_uom_unit")
        cls.packaging_1 = cls.env["product.uom"].create(
            {
                "barcode": "TESTPACK1",
                "product_id": cls.product.id,
                "uom_id": cls.uom.id,
            }
        )

    def test_packaging_archive(self):
        packaging = self.env["product.uom"].search([("id", "=", self.packaging_1.id)])
        self.assertTrue(packaging)
        self.packaging_1.active = False
        packaging = self.env["product.uom"].search([("id", "=", self.packaging_1.id)])
        self.assertFalse(packaging)
