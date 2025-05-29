# Copyright 2025 ForgeFlow (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestProductCategoryUoM(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_tmpl_obj = cls.env["product.template"]
        cls.default_uom = cls.product_tmpl_obj._get_default_uom_id()
        cls.uom = cls.env.ref("uom.product_uom_gram")
        vals = {
            "name": "Category Test",
            "code": "TEST",
            "uom_id": cls.uom.id,
        }
        cls.category = cls.env["product.category"].create(vals)

    def test_01_create(self):
        """Default UoM taken from the category"""
        product_test = self.product_tmpl_obj.create(
            {"name": "TEST 01", "categ_id": self.category.id}
        )
        product_test._onchange_categ_id_set_uom()
        self.assertEqual(product_test.uom_id, self.uom)

    def test_02_update(self):
        """Update UoM from category"""
        product_test = self.product_tmpl_obj.create({"name": "TEST 02"})
        self.assertEqual(product_test.uom_id, self.default_uom)
        product_test.categ_id = self.category.id
        self.category.update_product_uom()
        self.assertEqual(product_test.uom_id, self.uom)
