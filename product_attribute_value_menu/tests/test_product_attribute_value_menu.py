# Copyright 2026 360ERP (https://www.360erp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestProductAttributeValueMenu(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.attribute = cls.env["product.attribute"].create(
            {
                "name": "Test Color",
                "value_ids": [
                    (0, 0, {"name": "Test Red"}),
                    (0, 0, {"name": "Test Blue"}),
                ],
            }
        )
        cls.red, cls.blue = cls.attribute.value_ids
        cls.template_1 = cls._create_template("Test Product 1", cls.red | cls.blue)
        cls.template_2 = cls._create_template("Test Product 2", cls.red)

    @classmethod
    def _create_template(cls, name, values):
        return cls.env["product.template"].create(
            {
                "name": name,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attribute.id,
                            "value_ids": [(6, 0, values.ids)],
                        },
                    )
                ],
            }
        )

    def test_product_count(self):
        self.assertEqual(self.red.product_count, 2)
        self.assertEqual(self.blue.product_count, 1)

    def test_action_view_product_many(self):
        action = self.red.action_view_product()
        self.assertEqual(action["res_model"], "product.template")
        self.assertEqual(
            action["domain"], [("id", "in", (self.template_1 | self.template_2).ids)]
        )

    def test_action_view_product_one(self):
        action = self.blue.action_view_product()
        form_view = self.env.ref("product.product_template_only_form_view")
        self.assertEqual(action["res_id"], self.template_1.id)
        self.assertEqual(action["views"][0], (form_view.id, "form"))

    def test_extra_price_views(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "product_attribute_value_menu.import_product_attribute_value_action"
        )
        self.assertEqual(action["res_model"], "product.template.attribute.value")
        views = self.env["product.template.attribute.value"].get_views(action["views"])
        fields = views["models"][action["res_model"]]["fields"]
        self.assertIn("excluded_value_ids", fields)
