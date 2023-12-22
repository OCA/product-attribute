from odoo.tests.common import SavepointCase


class TestProductSearchByDisplayName(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.productA = cls.env["product.product"].create(
            {
                "name": "Product A",
                "default_code": "CodeA",
            }
        )
        cls.productA_template = cls.productA.product_tmpl_id

    def test_search_by_display_name_variant(self):
        expected_display_name = "[CodeA] Product A"
        product_read = self.env["product.product"].search_read(
            [("display_name", "=", expected_display_name)],
            ["id"],
            limit=1,
        )
        self.assertEqual(product_read[0]["id"], self.productA.id)

    def test_search_by_display_name_template(self):
        expected_display_name = "[CodeA] Product A"
        product_temlate_read = self.env["product.template"].search_read(
            [("display_name", "=", expected_display_name)],
            ["id"],
            limit=1,
        )
        self.assertEqual(product_temlate_read[0]["id"], self.productA_template.id)
