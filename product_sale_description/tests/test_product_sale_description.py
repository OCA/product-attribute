from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestProductSaleDescription(TransactionCase):
    """Test suite for product_sale_description fields and views."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=False))

    def test_description_fields_and_views(self):
        """Short and long description fields work on templates, variants, and views."""
        ProductTemplate = self.env["product.template"]
        short_field = ProductTemplate._fields["description_sale_short"]
        long_field = ProductTemplate._fields["description_sale_long"]
        self.assertEqual(short_field.type, "text")
        self.assertTrue(short_field.translate)
        self.assertEqual(long_field.type, "html")
        self.assertTrue(long_field.translate)

        product = ProductTemplate.create(
            {
                "name": "Described Product",
                "description_sale_short": "Compact summary",
                "description_sale_long": "<p>Detailed product copy</p>",
            }
        )
        self.assertEqual(product.description_sale_short, "Compact summary")
        self.assertIn("Detailed product copy", product.description_sale_long)
        self.assertEqual(
            product.product_variant_id.description_sale_short,
            "Compact summary",
        )

        views_result = ProductTemplate.get_views(
            [
                (self.env.ref("product.product_template_form_view").id, "form"),
                (self.env.ref("product.product_template_only_form_view").id, "form"),
            ]
        )
        form_fields = views_result["models"]["product.template"]["fields"]
        self.assertIn("description_sale_short", form_fields)
        self.assertIn("description_sale_long", form_fields)
