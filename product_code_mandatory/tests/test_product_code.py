# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import new_test_user

from odoo.addons.base.tests.common import BaseCommon


class TestProductCode(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Test with the lowest permissions needed to create products
        cls.env = cls.env(
            user=new_test_user(
                cls.env,
                login="product_code_mandatory_user",
                groups="base.group_user,product.group_product_manager",
            )
        )
        cls.product_model = cls.env["product.product"]
        cls.template_model = cls.env["product.template"]
        cls.product = cls.product_model.create({"name": "Test Product Code"})

    def test_product_code(self):
        """Check Product Code"""
        self.assertTrue(self.product.default_code, "Product code is not set.")

    def test_template_with_provided_code(self):
        """Check that product.template respects provided default_code"""
        custom_code = "TEMPLATE-CODE-456"
        template = self.template_model.create(
            {"name": "Test Template with Custom Code", "default_code": custom_code}
        )
        # Template variant should have the same code
        self.assertEqual(
            template.product_variant_id.default_code,
            custom_code,
            "Template variant should respect the provided default_code.",
        )

    def test_template_with_attributes_does_not_share_provided_code(self):
        """Variants of a template with attributes get their own code"""
        attribute = self.env["product.attribute"].create(
            {
                "name": "Test Attribute",
                "value_ids": [(0, 0, {"name": "A"}), (0, 0, {"name": "B"})],
            }
        )
        template = self.template_model.create(
            {
                "name": "Template with attributes",
                "default_code": "TEMPLATE-CODE",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attribute.id,
                            "value_ids": [(6, 0, attribute.value_ids.ids)],
                        },
                    )
                ],
            }
        )
        codes = template.product_variant_ids.mapped("default_code")
        self.assertEqual(len(set(codes)), 2, "Each variant needs its own code")
        self.assertNotIn("TEMPLATE-CODE", codes)
