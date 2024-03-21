# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.product_template_tags.tests.test_product_template_tags import (
    TestProductTemplateTagBase,
)


class TestProductTemplateTag(TestProductTemplateTagBase):
    def test_00_product_template_tag(self):
        self.assertEqual(self.tag.code, "test-tag")

    def test_01_product_template_tag_writable(self):
        self.tag.write(
            {
                "name": "Test Tag",
                "code": "foo tag !!",
                "product_tmpl_ids": [(6, 0, [self.product_tmpl.id])],
            }
        )
        self.assertEqual(self.tag.code, "foo-tag")
        self.tag.write({"code": "test tag writable"})
        self.assertEqual(self.tag.code, "test-tag-writable")
        self.tag.write({"name": "test tag name 2"})
        self.assertEqual(self.tag.code, "test-tag-name-2")

    def test_02_product_template_multi_tags(self):
        prods_data = []
        for x in range(3):
            prods_data.append(
                {
                    "name": "YO%s" % x,
                    "product_tmpl_ids": [(6, 0, [self.product_tmpl.id])],
                }
            )
        prods = self.env["product.template.tag"].create(prods_data)
        self.assertEqual(prods.mapped("code"), ["yo0", "yo1", "yo2"])
