# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64
from odoo.tests import SavepointCase


class TestProductModelViewer(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        binary_value = base64.b64encode(b'content')
        vals_list = [{
            "name": "Product 1",
            "gltf_3d_model_variant": binary_value
        }, {
            "name": "Product 2",
            "gltf_3d_model_variant": binary_value
        },
        ]
        cls.products = cls.env["product.product"].create(vals_list)

    def test_value_variant(self):
        for product in self.products:
            self.assertTrue(product.gltf_3d_model)
