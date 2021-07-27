# Copyright 2021 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from uuid import uuid4

from odoo.tests.common import SavepointCase


class TestPricelistAssortment(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPricelistAssortment, cls).setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
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

    def _define_prices(self, normal_price=1.0, assortment_price=1.0):
        self.normal_price = normal_price
        self.assortment_price = assortment_price

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
        item_global.write({"compute_price": "fixed", "fixed_price": self.normal_price})
        item_values = {
            "assortment_filter_id": self.assortment.id,
            "compute_price": "fixed",
            "fixed_price": self.assortment_price,
            "pricelist_id": pricelist.id,
        }
        self.assortment_item = self.PricelistItem.create(item_values)
        self.existing_items = pricelist.item_ids
        return True

    def _update_assortment(self, pricelist):
        pricelist.action_launch_assortment_update()

    def _test_values(self, pricelist):
        new_items = pricelist.item_ids - self.existing_items
        self.assertEqual(len(pricelist.item_assortment_ids), 1)
        # Check items created
        ensure_product_in = self.products_assortment
        self.assertTrue(bool(new_items))
        for item in new_items:
            self.assertIn(item.product_id, ensure_product_in)
            ensure_product_in -= item.product_id
            self.assertEqual(item.assortment_item_id, self.assortment_item)
        products_assortment = self.products_assortment.with_context(
            pricelist=pricelist.id
        )
        self.assertTrue(bool(products_assortment))
        for product in products_assortment:
            self.assertAlmostEqual(
                product.price, self.assortment_price, places=self.precision
            )
        normal_product = self.Product.search(
            [("id", "not in", self.products_assortment.ids)], limit=1
        ).with_context(pricelist=pricelist.id)
        self.assertAlmostEqual(
            normal_product.price, self.normal_price, places=self.precision
        )

    def test_pricelist_assortment(self):
        """
        Check if prices are correctly returned for a product into an
        assortment.
        :return:
        """
        self._define_prices(normal_price=111.111, assortment_price=526.369)
        pricelist_values = self._get_pricelist_values()
        pricelist = self.Pricelist.create(pricelist_values)
        self._add_assortment_item_fixed_price(pricelist)
        self._update_assortment(pricelist)
        self._test_values(pricelist)
        return

    def test_cron(self):
        """
        * Create a new pricelist
        * Create a new pricelist assortment item
        * Launch cron update
        * New pricelist items should have been created
        """
        self._define_prices(normal_price=111.111, assortment_price=526.369)
        pricelist_values = self._get_pricelist_values()
        pricelist = self.Pricelist.create(pricelist_values)
        self._add_assortment_item_fixed_price(pricelist)
        pricelist.flush()
        self.env["product.pricelist"].cron_assortment_update()
        self._test_values(pricelist)
