# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.product_template_tags.tests.test_product_template_tags import (
    TestProductTemplateTagBase,
)


class TestProductTemplateTag(TestProductTemplateTagBase):
    def test_product_template_tag(self):
        product_tmpl_tag = self.env["product.template.tag"].create(
            {"name": "Test Tag", "product_tmpl_ids": [(6, 0, [self.product_tmpl.id])]}
        )
        self.assertEqual(product_tmpl_tag.code, "test-tag")

    def test_product_template_tag_writable(self):
        product_tmpl_tag = self.env["product.template.tag"].create(
            {
                "name": "Test Tag",
                "code": "foo tag !!",
                "product_tmpl_ids": [(6, 0, [self.product_tmpl.id])],
            }
        )
        self.assertEqual(product_tmpl_tag.code, "foo-tag")
        product_tmpl_tag.write({"code": "test tag writable"})
        self.assertEqual(product_tmpl_tag.code, "test-tag-writable")
        product_tmpl_tag.write({"name": "test tag name 2"})
        self.assertEqual(product_tmpl_tag.code, "test-tag-name-2")

    def test_product_template_multi_tags(self):
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
