from odoo.tests.common import TransactionCase


class TestProductAttributeValue(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        ProductTemplate = cls.env["product.template"]
        Attribute = cls.env["product.attribute"]
        AttributeValue = cls.env["product.attribute.value"]

        # Create attribute and value
        cls.attribute = Attribute.create({"name": "Color"})
        cls.value = AttributeValue.create(
            {
                "name": "Red",
                "attribute_id": cls.attribute.id,
            }
        )

        # Attribute line values for product creation
        cls.attribute_line_vals = {
            "attribute_id": cls.attribute.id,
            "value_ids": [(6, 0, cls.value.ids)],
        }

        # Create products
        cls.product_1 = ProductTemplate.create(
            {
                "name": "Test Product A",
                "attribute_line_ids": [(0, 0, cls.attribute_line_vals)],
            }
        )
        cls.product_2 = ProductTemplate.create(
            {
                "name": "Test Product B",
                "attribute_line_ids": [(0, 0, cls.attribute_line_vals)],
            }
        )

    def test_product_count(self):
        """Test that product_count reflects the number of products linked to
        the attribute value."""
        self.assertEqual(
            self.value.product_count,
            2,
            "Product count should be equal to number of linked products",
        )

    def test_action_view_product_multiple(self):
        """Test that action_view_product returns a
        product list when multiple products are linked."""
        action = self.value.action_view_product()
        self.assertIn(
            "domain",
            action,
            "product_count does not match the number of linked products",
        )
        self.assertEqual(
            action["domain"],
            [("id", "in", [self.product_1.id, self.product_2.id])],
            "Domain does not include both linked products",
        )

    def test_action_view_product_single(self):
        """Test that action_view_product opens the product
        form directly when there is a single linked product."""
        self.product_2.attribute_line_ids.unlink()
        action = self.value.action_view_product()
        self.assertEqual(
            action.get("res_id"),
            self.product_1.id,
            "Action did not open the single linked product's form view",
        )
