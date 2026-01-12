# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo.addons.base.tests.common import BaseCommon


class TestProductPackagingArchive(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create({"name": "Test Product"})
        cls.packaging_1 = cls.env["product.packaging"].create(
            {
                "name": "Packaging 1",
                "product_id": cls.product.id,
            }
        )

    def test_packaging_archive(self):
        packaging = self.env["product.packaging"].search(
            [("id", "=", self.packaging_1.id)]
        )
        self.assertTrue(packaging)
        self.packaging_1.active = False
        packaging = self.env["product.packaging"].search(
            [("id", "=", self.packaging_1.id)]
        )
        self.assertFalse(packaging)
