# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.product_template_tags.tests.test_product_template_tags import (
    TestProductTemplateTagBase,
)


class TestProductProductTagsBase(TestProductTemplateTagBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.tag1 = cls.env["product.template.tag"].create({"name": "Tag 1"})
        cls.tag2 = cls.env["product.template.tag"].create({"name": "Tag 2"})
        cls.tag3 = cls.env["product.template.tag"].create({"name": "Tag 3"})

        cls.product_tmpl.tag_ids = [(6, 0, [cls.tag1.id])]

        product_attribute = cls.env["product.attribute"].create(
            {
                "name": "Color",
                "display_type": "color",
            }
        )

        color_red = "#CD5C5C"
        name_red = "Indian Red"

        attr_values = cls.env["product.attribute.value"].create(
            [
                {
                    "name": name_red,
                    "attribute_id": product_attribute.id,
                    "html_color": color_red,
                },
            ]
        )

        cls.env["product.template.attribute.line"].create(
            [
                {
                    "attribute_id": product_attribute.id,
                    "product_tmpl_id": cls.product_tmpl.id,
                    "value_ids": [(6, 0, attr_values.ids)],
                }
            ]
        )

        cls.product_product = cls.env["product.product"].create(
            {
                "name": "Test variant",
                "product_tmpl_id": cls.product_tmpl.id,
            }
        )
        cls.product_tmpl.product_variant_id = cls.product_product.id


class TestProductProductTags(TestProductProductTagsBase):
    def test_create_product_product(self):
        """Test product product var_tag value at creation"""
        self.assertEqual(
            self.product_tmpl.tag_ids.ids,
            self.product_product.tag_ids.ids,
            "Tag1 wasn't as a variant at product.product creation",
        )

    def test_add_product_template_tag(self):
        """Add a tag in template"""
        self.product_tmpl.tag_ids = [(6, 0, [self.tag2.id])]
        self.assertIn(
            self.tag2.id, self.product_tmpl.tag_ids.ids, "Tag2 wasn't added to template"
        )
        self.assertIn(
            self.tag2.id,
            self.product_product.tag_ids.ids,
            "Tag2 wasn't added to variant",
        )

    def test_remove_template_tag(self):
        """Remove a tag in template"""
        self.product_tmpl.tag_ids = [(6, 0, [self.tag2.id])]
        self.product_tmpl.write({"tag_ids": [(3, self.tag2.id)]})
        self.assertNotIn(
            self.tag2.id,
            self.product_tmpl.tag_ids.ids,
            "Tag2 wasn't removed from template",
        )
        self.assertNotIn(
            self.tag2.id,
            self.product_product.tag_ids.ids,
            "Tag2 was added in variant",
        )

    def test_add_product_product_tag(self):
        """Add a tag in variant"""
        self.product_product.tag_ids = [(6, 0, [self.tag3.id])]
        self.assertNotIn(
            self.tag3.id,
            self.product_tmpl.tag_ids.ids,
            "Tag3 was also added to template",
        )
        self.assertIn(
            self.tag3.id,
            self.product_product.tag_ids.ids,
            "Tag3 wasn't added to variant",
        )

    def test_remove_product_product_tag(self):
        """Remove a tag in variant"""
        self.product_product.tag_ids = [(6, 0, [self.tag3.id])]
        self.product_product.write({"tag_ids": [(3, self.tag1.id)]})
        self.assertIn(
            self.tag1.id,
            self.product_tmpl.tag_ids.ids,
            "Tag1 was aslo removed from template",
        )
        self.assertNotIn(
            self.tag1.id,
            self.product_product.tag_ids.ids,
            "Tag1 wasn't removed from variant",
        )
