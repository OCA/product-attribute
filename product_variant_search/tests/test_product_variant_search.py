# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.fields import Command

from odoo.addons.base.tests.common import BaseCommon


class TestProductVariantSearch(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ja = (
            cls.env["res.lang"]
            .with_context(active_test=False)
            .search([("code", "=", "ja_JP")])
        )
        cls.env["base.language.install"].create({"lang_ids": ja.ids}).lang_install()
        # Attributes: Color (Red/Blue), Size (S/M)
        Attr = cls.env["product.attribute"]
        Val = cls.env["product.attribute.value"]
        cls.attr_color = Attr.create({"name": "Color"})
        cls.val_red = Val.create({"name": "Red", "attribute_id": cls.attr_color.id})
        cls.val_blue = Val.create({"name": "Blue", "attribute_id": cls.attr_color.id})
        cls.attr_size = Attr.create({"name": "Size"})
        cls.val_s = Val.create({"name": "S", "attribute_id": cls.attr_size.id})
        cls.val_m = Val.create({"name": "M", "attribute_id": cls.attr_size.id})
        cls.val_red.with_context(lang="ja_JP").write({"name": "赤"})
        cls.val_blue.with_context(lang="ja_JP").write({"name": "青"})
        cls.val_s.with_context(lang="ja_JP").write({"name": "小"})
        cls.val_m.with_context(lang="ja_JP").write({"name": "中"})
        cls.tmpl = cls.env["product.template"].create(
            {
                "name": "Test Product",
                "attribute_line_ids": [
                    Command.create(
                        {
                            "attribute_id": cls.attr_color.id,
                            "value_ids": [
                                Command.set([cls.val_red.id, cls.val_blue.id]),
                            ],
                        }
                    ),
                    Command.create(
                        {
                            "attribute_id": cls.attr_size.id,
                            "value_ids": [
                                Command.set([cls.val_s.id, cls.val_m.id]),
                            ],
                        }
                    ),
                ],
            }
        )

    def test_name_search_variant_by_en(self):
        Product = self.env["product.product"].with_context(lang="en_US")
        self.assertEqual(len(Product.name_search("Test Product")), 4)
        self.assertEqual(len(Product.name_search("Test Product (Red,")), 2)
        self.assertEqual(len(Product.name_search("Test Product (Blue,")), 2)
        self.assertEqual(len(Product.name_search("Test Product (Red, S)")), 1)
        self.assertEqual(len(Product.name_search("Test Product (Blue, M)")), 1)

    def test_name_search_variant_by_jp(self):
        Product = self.env["product.product"].with_context(lang="ja_JP")
        self.assertEqual(len(Product.name_search("Test Product")), 4)
        self.assertEqual(len(Product.name_search("Test Product (赤,")), 2)
        self.assertEqual(len(Product.name_search("Test Product (青,")), 2)
        self.assertEqual(len(Product.name_search("Test Product (赤, 小)")), 1)
        self.assertEqual(len(Product.name_search("Test Product (青, 中)")), 1)
