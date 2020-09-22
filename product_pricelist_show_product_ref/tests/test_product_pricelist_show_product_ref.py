# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestProductPricelistShowProductRef(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductPricelistShowProductRef, cls).setUpClass()
        cls.product_obj = cls.env["product.product"]
        cls.product_template_obj = cls.env["product.template"]
        cls.pricelist_obj = cls.env["product.pricelist"]
        cls.pricelist_item_obj = cls.env["product.pricelist.item"]

        # Create a price list, a product category, a product template and
        # a product variant
        cls.product = cls.product_obj.create({
            "name": "Product 1",
            "default_code": "ABC"
        })
        cls.product_template = cls.product_template_obj.create({
            "name": "Product Template",
            "default_code": "DEF"
        })
        cls.pricelist = cls.pricelist_obj.create({
            "name": "Pricelist",
            "item_ids": False,
        })
        # Create pricelist items
        cls.pricelist_item_product_template = cls.pricelist_item_obj.create({
            'pricelist_id': cls.pricelist.id,
            'applied_on': '1_product',
            'product_tmpl_id': cls.product_template.id,
            'compute_price': 'percentage',
            'percent_price': 5,
        })
        cls.pricelist_item_product_product = cls.pricelist_item_obj.create({
            'pricelist_id': cls.pricelist.id,
            'applied_on': '0_product_variant',
            'product_id': cls.product.id,
            'compute_price': 'fixed',
            'fixed_price': 100,
        })

    def test_code_in_display_name_in_product(self):
        """Test product item has code in display_name
        """
        self.assertTrue(
            "[{}]".format(
                self.pricelist_item_product_product.product_id.default_code
            ) in self.pricelist_item_product_product.display_name
        )

    def test_code_not_in_display_name_in_product_template(self):
        """Test product template item has no code in display_name
        """
        self.assertFalse(
            "[{}]".format(
                self.pricelist_item_product_template.product_id.default_code
            ) in self.pricelist_item_product_template.display_name
        )

    def test_display_name_rewritten(self):
        """Test the display_name is rewritten
        """
        product_name = self.product.display_name.replace(
            "[{}]".format(self.product.default_code),
            ""
        )
        self.pricelist_item_product_product.display_name = product_name
        self.assertFalse(
            "[{}]".format(
                self.pricelist_item_product_product.product_id.default_code
            ) in self.pricelist_item_product_product.display_name
        )
        self.pricelist_item_product_product._get_pricelist_item_name_price()
        self.assertTrue(
            "[{}]".format(
                self.pricelist_item_product_product.product_id.default_code
            ) in self.pricelist_item_product_product.display_name
        )
