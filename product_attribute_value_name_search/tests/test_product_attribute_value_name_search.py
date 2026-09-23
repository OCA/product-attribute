# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Command

from odoo.addons.base.tests.common import BaseCommon


class TestProductTemplateAttributeValueNameSearch(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Attr = cls.env["product.attribute"]
        Val = cls.env["product.attribute.value"]
        cls.attr_color = Attr.create({"name": "Color"})
        cls.attr_size = Attr.create({"name": "Size"})
        cls.pav_color_red = Val.create(
            {"name": "Red", "attribute_id": cls.attr_color.id}
        )
        cls.pav_size_red = Val.create({"name": "Red", "attribute_id": cls.attr_size.id})
        cls.pav_size_large = Val.create(
            {"name": "L: Large", "attribute_id": cls.attr_size.id}
        )
        # Create a product template with attribute lines to generate PTAVs
        cls.tmpl = cls.env["product.template"].create(
            {
                "name": "Test Product",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": cls.attr_color.id,
                            "value_ids": [Command.set([cls.pav_color_red.id])],
                        }
                    ),
                    Command.create(
                        {
                            "attribute_id": cls.attr_size.id,
                            "value_ids": [
                                Command.set(
                                    [cls.pav_size_red.id, cls.pav_size_large.id]
                                )
                            ],
                        }
                    ),
                ],
            }
        )
        PTAV = cls.env["product.template.attribute.value"]
        cls.ptav_color_red = PTAV.search(
            [
                ("product_tmpl_id", "=", cls.tmpl.id),
                ("product_attribute_value_id", "=", cls.pav_color_red.id),
            ]
        )
        cls.ptav_size_red = PTAV.search(
            [
                ("product_tmpl_id", "=", cls.tmpl.id),
                ("product_attribute_value_id", "=", cls.pav_size_red.id),
            ]
        )
        cls.ptav_size_large = PTAV.search(
            [
                ("product_tmpl_id", "=", cls.tmpl.id),
                ("product_attribute_value_id", "=", cls.pav_size_large.id),
            ]
        )

    def test_exact_match(self):
        """Search with 'Attribute: Value' format returns only the correct one."""
        PTAV = self.env["product.template.attribute.value"]
        result = PTAV.name_search("Color: Red", operator="=")
        result_ids = [r[0] for r in result]
        self.assertIn(self.ptav_color_red.id, result_ids)
        self.assertNotIn(self.ptav_size_red.id, result_ids)

    def test_ilike_match(self):
        """Search with ilike operator on composite name works."""
        PTAV = self.env["product.template.attribute.value"]
        result = PTAV.name_search("Color: Re", operator="ilike")
        result_ids = [r[0] for r in result]
        self.assertIn(self.ptav_color_red.id, result_ids)
        self.assertNotIn(self.ptav_size_red.id, result_ids)

    def test_fallback_without_separator(self):
        """Search without separator falls back to default behavior."""
        PTAV = self.env["product.template.attribute.value"]
        result = PTAV.name_search("Red", operator="ilike")
        result_ids = [r[0] for r in result]
        self.assertIn(self.ptav_color_red.id, result_ids)
        self.assertIn(self.ptav_size_red.id, result_ids)

    def test_colon_in_value_name(self):
        """Value name containing ': ' is handled by splitting on first occurrence."""
        PTAV = self.env["product.template.attribute.value"]
        result = PTAV.name_search("Size: L: Large", operator="=")
        result_ids = [r[0] for r in result]
        self.assertIn(self.ptav_size_large.id, result_ids)
