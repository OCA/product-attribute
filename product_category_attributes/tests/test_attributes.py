# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestCategoryAttributes(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.product_tmpl = self.env.ref(
            "product.product_product_4_product_template",
        )
        self.category = self.env.ref("product.product_category_5")
        self.attr_1 = self.env.ref("product.product_attribute_1")
        self.attr_2 = self.env.ref("product.product_attribute_2")
        self.attr_1_val_1 = self.env.ref("product.product_attribute_value_1")

    def test_attribute_onchange(self):
        line = self.env["product.category.attribute.line"].create(
            {
                "category_id": self.category.id,
                "attribute_id": self.attr_1.id,
                "value_ids": [(4, self.attr_1_val_1.id)],
            }
        )

        with common.Form(line) as f:
            f.attribute_id = self.attr_2

        self.assertFalse(line.value_ids)

    def test_compute_allowed_attributes(self):
        self.category.write(
            {
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "category_id": self.category.id,
                            "attribute_id": self.attr_1.id,
                        },
                    )
                ],
            }
        )

        line = self.env["product.template.attribute.line"].new(
            {"product_tmpl_id": self.product_tmpl.id}
        )

        self.assertEqual(line.allowed_attribute_ids, self.attr_1)
        self.assertFalse(line.allowed_attribute_value_ids)

    def test_compute_allowed_attribute_values(self):
        self.category.write(
            {
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "category_id": self.category.id,
                            "attribute_id": self.attr_1.id,
                            "value_ids": [(6, 0, self.attr_1_val_1.ids)],
                        },
                    )
                ],
            }
        )

        line = self.env["product.template.attribute.line"].new(
            {"product_tmpl_id": self.product_tmpl.id, "attribute_id": self.attr_1.id}
        )

        self.assertEqual(line.allowed_attribute_value_ids, self.attr_1_val_1)
