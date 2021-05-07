# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from uuid import uuid4

from odoo.fields import first
from odoo.tests.common import SavepointCase


class TestPricelistAssortment(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPricelistAssortment, cls).setUpClass()
        cls.Pricelist = cls.env["product.pricelist"]
        cls.PricelistItem = cls.env["product.pricelist.assortment.item"]
        cls.Product = cls.env["product.product"]
        cls.Assortment = cls.env["ir.filters"]
        cls.default_codes = [str(uuid4()) for x in range(0, 10)]
        cls.precision = 2
        cls.assortment = cls._create_assortment(cls)
        cls.products_assortment = cls._create_products_assortment(cls)

    def _create_assortment(self):
        """
        Create a new assortment
        :return: ir.filters recordset
        """
        values = {
            "name": str(uuid4()),
            "model_id": "product.product",
            "domain": [("default_code", "in", self.default_codes)],
            "user_id": False,
            "is_assortment": True,
        }
        return self.Assortment.create(values)

    def _create_products_assortment(self):
        """
        Create some product.product matching with assortment.
        :return: product.product recordset
        """
        products = self.Product.browse()
        for default_code in self.default_codes:
            values = {
                "name": str(uuid4()),
                "default_code": default_code,
            }
            products |= self.Product.create(values)
        return products

    def _get_pricelist_values(self):
        """
        Get values to create a new pricelist
        :return: dict
        """
        fields_list = self.Pricelist.fields_get().keys()
        values = self.Pricelist.default_get(fields_list)
        values.update({"name": str(uuid4()), "active": True, "item_ids": [(0, 0, {})]})
        return values

    def _add_assortment_item_fixed_price(self, pricelist):
        """
        - Add a new item assortment
        - Check if action_launch_assortment_update is correct
        - Check if the given product price is correct (concerned by assortment)
        - Check if a normal product still correct
        :param pricelist: product.pricelist recordset
        :return: bool
        """
        item_global = pricelist.item_ids.filtered(lambda i: i.applied_on == "3_global")
        normal_price = 111.111
        assortment_price = 526.369
        item_global.write({"compute_price": "fixed", "fixed_price": normal_price})
        item_values = {
            "assortment_filter_id": self.assortment.id,
            "compute_price": "fixed",
            "fixed_price": assortment_price,
            "pricelist_id": pricelist.id,
        }
        assortment_item = self.PricelistItem.create(item_values)
        existing_items = pricelist.item_ids
        pricelist.action_launch_assortment_update()
        new_items = pricelist.item_ids - existing_items
        self.assertEquals(len(pricelist.item_assortment_ids), 1)
        # Check items created
        ensure_product_in = self.products_assortment
        self.assertTrue(bool(new_items))
        for item in new_items:
            self.assertIn(item.product_id, ensure_product_in)
            ensure_product_in -= item.product_id
            self.assertEquals(item.assortment_item_id, assortment_item)
        products_assortment = self.products_assortment.with_context(
            pricelist=pricelist.id
        )
        self.assertTrue(bool(products_assortment))
        for product in products_assortment:
            self.assertAlmostEquals(
                product.price, assortment_price, places=self.precision
            )
        normal_product = self.Product.search(
            [("id", "not in", self.products_assortment.ids)], limit=1
        ).with_context(pricelist=pricelist.id)
        self.assertAlmostEquals(
            normal_product.price, normal_price, places=self.precision
        )
        return True

    def test_pricelist_assortment(self):
        """
        Check if prices are correctly returned for a product into an
        assortment.
        :return:
        """
        pricelist_values = self._get_pricelist_values()
        pricelist = self.Pricelist.create(pricelist_values)
        self._add_assortment_item_fixed_price(pricelist)
        return

    def test_assortment_changes(self):
        pricelist_values = self._get_pricelist_values()
        pricelist = self.Pricelist.create(pricelist_values)
        item_values = {
            "assortment_filter_id": self.assortment.id,
            "compute_price": "fixed",
            "fixed_price": 600,
            "pricelist_id": pricelist.id,
        }
        assortment_item = self.PricelistItem.create(item_values)
        (
            products_to_add,
            products_to_update,
            products_to_remove,
        ) = assortment_item._get_assortment_changes()

        self.assertEqual(self.products_assortment, products_to_add)
        self.assertFalse(products_to_update)
        self.assertFalse(products_to_remove)

        pricelist.action_launch_assortment_update()

        # change product to exclude it from assortment
        product1 = first(self.products_assortment)
        product1.write({"default_code": "test"})
        expected_update = self.products_assortment - product1

        (
            products_to_add,
            products_to_update,
            products_to_remove,
        ) = assortment_item._get_assortment_changes()
        self.assertEqual(product1, products_to_remove)
        self.assertFalse(products_to_add)
        self.assertEqual(products_to_update, expected_update)

        create_values, update_values = assortment_item._get_pricelist_item_values()

        update_items = pricelist.item_ids.filtered(
            lambda x: x.product_id in products_to_update
        )
        item = first(update_items)
        self.assertFalse(assortment_item._check_need_update(item, update_values))
        pricelist.action_launch_assortment_update()

        assortment_item.write({"fixed_price": 650})
        (
            products_to_add,
            products_to_update,
            products_to_remove,
        ) = assortment_item._get_assortment_changes()
        self.assertFalse(products_to_remove)
        self.assertFalse(products_to_add)
        self.assertEqual(products_to_update, expected_update)

        create_values, update_values = assortment_item._get_pricelist_item_values()

        update_items = pricelist.item_ids.filtered(
            lambda x: x.product_id in products_to_update
        )
        item = first(update_items)
        self.assertTrue(assortment_item._check_need_update(item, update_values))
