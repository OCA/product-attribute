# Copyright 2024 Cetmix OÜ
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import exceptions
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestOptionalProductQuantity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_template_1 = cls.env["product.template"].create(
            {
                "name": "Product 1",
                "type": "product",
                "categ_id": cls.env.ref("product.product_category_all").id,
            }
        )
        cls.product_template_2 = cls.env["product.template"].create(
            {
                "name": "Product 2",
                "type": "product",
                "categ_id": cls.env.ref("product.product_category_all").id,
            }
        )
        cls.product_template_3 = cls.env["product.template"].create(
            {
                "name": "Product 3",
                "type": "product",
                "categ_id": cls.env.ref("product.product_category_all").id,
            }
        )

    def test_product_optional_line_constrains(self):
        # Try to set parent product as an optional
        with self.assertRaises(exceptions.ValidationError):
            self.env["product.optional.line"].create(
                {
                    "product_tmpl_id": self.product_template_1.id,
                    "optional_product_tmpl_id": self.product_template_1.id,
                }
            )

        # Try to set two same products as optional
        with self.assertRaises(exceptions.ValidationError):
            self.env["product.optional.line"].create(
                [
                    {
                        "product_tmpl_id": self.product_template_1.id,
                        "optional_product_tmpl_id": self.product_template_2.id,
                    },
                    {
                        "product_tmpl_id": self.product_template_1.id,
                        "optional_product_tmpl_id": self.product_template_2.id,
                    },
                ]
            )

    def test_optional_product_ids_computation(self):
        # Create first optional product for Product 1
        self.env["product.optional.line"].create(
            {
                "product_tmpl_id": self.product_template_1.id,
                "optional_product_tmpl_id": self.product_template_2.id,
            }
        )
        # optional_product_ids of Product 1 should contain 1 record with name 'Product 2'
        self.assertTrue(
            len(self.product_template_1.optional_product_ids) == 1
            and self.product_template_1.optional_product_ids[0].name == "Product 2",
            msg="optional_product_ids of product.template has been computed incorrectly",
        )
        # Create second optional product for Product 1
        self.env["product.optional.line"].create(
            {
                "product_tmpl_id": self.product_template_1.id,
                "optional_product_tmpl_id": self.product_template_3.id,
            }
        )
        # optional_product_ids of Product 1 should contain 2 records
        # with names 'Product 2' and 'Product 3'
        self.assertTrue(
            len(self.product_template_1.optional_product_ids) == 2
            and self.product_template_1.optional_product_ids[0].name == "Product 2"
            and self.product_template_1.optional_product_ids[1].name == "Product 3",
            msg="optional_product_ids of product.template has been computed incorrectly",
        )
