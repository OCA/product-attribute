from unittest.mock import patch

from odoo.tests.common import TransactionCase


class TestProductModelIdentifier(TransactionCase):
    def setUp(self):
        super().setUp()
        self.env.company.eprel_api_key = "FAKE_KEY"
        eprel_category = self.env["product.category.eprel"].create(
            {
                "name": "Smartphones and slate tablets",
                "code": "smartphonestablets20231669",
            }
        )
        self.category = self.env["product.category"].create(
            {
                "name": "Smartphones",
                "eprel_category_id": eprel_category.id,
            }
        )
        self.product = self.env["product.template"].create(
            {
                "name": "Edge 60 Pro",
                "eprel_model_identifier": "edge 60 pro (XT2507-1)",
                "categ_id": self.category.id,
            }
        )

    def test_fetch_eprel_registration_number_with_patch(self):
        fake_response_data = {"hits": [{"eprelRegistrationNumber": "2266111"}]}

        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return fake_response_data

            @property
            def text(self):
                return '{"hits": [{"eprelRegistrationNumber": "2266111"}]}'

        with patch(
            "odoo.addons.product_eprel.models.product_template.requests.get",
            return_value=MockResponse(),
        ):
            self.product.action_get_eprel_registration_number()
        self.assertEqual(self.product.eprel_registration_number, "2266111")
        self.assertTrue(self.product.fiche_url)
        self.assertEqual(
            "https://eprel.ec.europa.eu/fiches/smartphonestablets20231669/Fiche_2266111_EN.pdf",
            self.product.fiche_url,
        )
