import logging

from odoo.tests.common import SavepointCase


class TestProductState(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ProductState = cls.env["product.state"]
        cls.state = cls.ProductState.create({"name": "State Name", "code": "Code"})

    def test_01_product_state(self):
        # print(self.state.products_count)
        logger = logging.getLogger(self.state.products_count)
