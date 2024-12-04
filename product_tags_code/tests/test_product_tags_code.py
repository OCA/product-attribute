# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestProductTagsCode(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_tmpl = cls.env["product.template"].create({"name": "Test Product"})

    def test_product_tags_code(self):
        product_tag = self.env["product.tag"].create(
            {
                "name": "Test Tag",
                "product_template_ids": [(6, 0, [self.product_tmpl.id])],
            }
        )
        self.assertEqual(product_tag.code, "test-tag")

    def test_product_tags_code_writable(self):
        product_tag = self.env["product.tag"].create(
            {
                "name": "Test Tag",
                "code": "foo tag !!",
                "product_template_ids": [(6, 0, [self.product_tmpl.id])],
            }
        )
        self.assertEqual(product_tag.code, "foo-tag")
        product_tag.write({"code": "test tag writable"})
        self.assertEqual(product_tag.code, "test-tag-writable")
        product_tag.write({"name": "test tag name 2"})
        self.assertEqual(product_tag.code, "test-tag-name-2")

    def test_product_multi_tags(self):
        prods_data = []
        for x in range(3):
            prods_data.append(
                {
                    "name": f"YO{x}",
                    "product_template_ids": [(6, 0, [self.product_tmpl.id])],
                }
            )
        prods = self.env["product.tag"].create(prods_data)
        self.assertEqual(prods.mapped("code"), ["yo0", "yo1", "yo2"])
