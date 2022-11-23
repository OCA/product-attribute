# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestTemplateValues(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product_template = cls.env["product.template"].create(
            {
                "name": "Unittest P1",
                "product_length": 10.0,
                "product_width": 5.0,
                "product_height": 3.0,
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "type": "consu",
            }
        )

    def test_template(self):
        """
        Data:
            one product template with dimensions
        Test Case:
            get the product associated to the product_template and
            check that the length, width and height
            are the same as for the product template
        Expected result:
            length, width, height are the same on the product and product template
        """

        product = self.product_template.product_variant_ids

        self.assertEqual(product.product_length, 10.0)
        self.assertEqual(product.product_width, 5.0)
        self.assertEqual(product.product_height, 3.0)
