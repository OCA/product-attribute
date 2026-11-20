from odoo.tools import float_compare

from odoo.addons.base.tests.common import BaseCommon


class TestPricelistGlobal(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(cls.env.context, test_compute_list_price_from_pricelist=True)
        )
        cls.Product = cls.env["product.product"]
        cls.ProductTemplate = cls.env["product.template"]
        cls.ProductCateg = cls.env["product.category"]
        cls.Pricelist = cls.env["product.pricelist"]
        cls.PricelistItem = cls.env["product.pricelist.item"]
        cls.company_2 = cls.env["res.company"].create({"name": "Company 2"})
        cls.categ_1 = cls.ProductCateg.create({"name": "Categ 1"})
        cls.categ_2 = cls.ProductCateg.create({"name": "Categ 2"})
        cls.product_1 = cls.Product.create(
            {
                "name": "Product 1",
                "list_price": 100,
                "standard_price": 80,
                "categ_id": cls.categ_1.id,
            }
        )
        cls.product_2 = cls.Product.create(
            {
                "name": "Product 2",
                "list_price": 200,
                "standard_price": 180,
                "categ_id": cls.categ_1.id,
            }
        )
        cls.product_3 = cls.Product.create(
            {
                "name": "Product 3",
                "list_price": 300,
                "standard_price": 280,
                "categ_id": cls.categ_2.id,
            }
        )
        # this product is not affected by the pricelist
        # the price should remain unchanged
        cls.product_4 = cls.Product.create(
            {
                "name": "Product 4",
                "list_price": 400,
                "categ_id": cls.categ_2.id,
            }
        )
        # this product just belongs to company 2
        cls.product_5 = cls.Product.create(
            {
                "name": "Product 4",
                "list_price": 500,
                "categ_id": cls.categ_2.id,
                "company_id": cls.company_2.id,
            }
        )
        cls.base_pricelist = cls.Pricelist.create({"name": "Base Pricelist"})
        cls.base_pricelist_item_global = cls.PricelistItem.create(
            {
                "pricelist_id": cls.base_pricelist.id,
                "applied_on": "3_global",
                "compute_price": "percentage",
                "percent_price": -5,
            }
        )
        cls.base_pricelist_item_product_3 = cls.PricelistItem.create(
            {
                "pricelist_id": cls.base_pricelist.id,
                "applied_on": "0_product_variant",
                "product_id": cls.product_3.id,
                "compute_price": "percentage",
                "percent_price": -10,
            }
        )
        cls.pricelist = cls.Pricelist.create({"name": "Pricelist"})
        cls.pricelist_item_by_product = cls.PricelistItem.create(
            {
                "pricelist_id": cls.pricelist.id,
                "applied_on": "0_product_variant",
                "product_id": cls.product_3.id,
                "compute_price": "percentage",
                "percent_price": 10,
            }
        )
        cls.pricelist_item_by_categ = cls.PricelistItem.create(
            {
                "pricelist_id": cls.pricelist.id,
                "applied_on": "2_product_category",
                "categ_id": cls.categ_1.id,
                "compute_price": "percentage",
                "percent_price": 20,
            }
        )
        # this pricelist is for company 2
        # and just affects the product_4, product_5 and categ_1(products 1 and 2)
        cls.pricelist_c2 = cls.Pricelist.create(
            {"name": "Pricelist C2", "company_id": cls.company_2.id}
        )
        cls.pricelist_item_by_product4_c2 = cls.PricelistItem.create(
            {
                "pricelist_id": cls.pricelist_c2.id,
                "applied_on": "1_product",
                "product_tmpl_id": cls.product_4.product_tmpl_id.id,
                "compute_price": "percentage",
                "percent_price": -10,
            }
        )
        cls.pricelist_item_by_product5_c2 = cls.PricelistItem.create(
            {
                "pricelist_id": cls.pricelist_c2.id,
                "applied_on": "1_product",
                "product_tmpl_id": cls.product_5.product_tmpl_id.id,
                "compute_price": "percentage",
                "percent_price": -10,
            }
        )
        cls.pricelist_item_by_categ_c2 = cls.PricelistItem.create(
            {
                "pricelist_id": cls.pricelist_c2.id,
                "applied_on": "2_product_category",
                "categ_id": cls.categ_1.id,
                "compute_price": "percentage",
                "percent_price": -5,
            }
        )
        cls.env.company.base_pricelist_compute_price_id = cls.pricelist
        cls.company_2.base_pricelist_compute_price_id = cls.pricelist_c2

    def test_02_pricelist_compute_price_percentage_with_discount(self):
        self.pricelist._update_product_price_from_pricelist()
        self.assertEqual(self.product_1.list_price, 80)
        self.assertEqual(self.product_2.list_price, 160)
        self.assertEqual(self.product_3.list_price, 270)
        self.assertEqual(self.product_4.list_price, 400)
        self.assertEqual(self.product_5.list_price, 500)

    def test_03_pricelist_compute_price_percentage_with_recharge(self):
        self.pricelist_item_by_product.write({"percent_price": -10})
        self.pricelist_item_by_categ.write({"percent_price": -20})
        self.assertEqual(self.product_1.list_price, 120)
        self.assertEqual(self.product_2.list_price, 240)
        self.assertEqual(self.product_3.list_price, 330)
        self.assertEqual(self.product_4.list_price, 400)
        self.assertEqual(self.product_5.list_price, 500)

    def test_04_pricelist_compute_price_fixed(self):
        self.pricelist_item_by_product.write(
            {"compute_price": "fixed", "fixed_price": 150}
        )
        self.pricelist_item_by_categ.write(
            {"compute_price": "fixed", "fixed_price": 250}
        )
        self.assertEqual(self.product_1.list_price, 250)
        self.assertEqual(self.product_2.list_price, 250)
        self.assertEqual(self.product_3.list_price, 150)
        self.assertEqual(self.product_4.list_price, 400)
        self.assertEqual(self.product_5.list_price, 500)

    def test_05_pricelist_compute_price_formula(self):
        self.pricelist_item_by_product.write(
            {"compute_price": "formula", "price_discount": -10}
        )
        self.pricelist_item_by_categ.write(
            {"compute_price": "formula", "price_discount": -20}
        )
        self.assertEqual(self.product_1.list_price, 120)
        self.assertEqual(self.product_2.list_price, 240)
        self.assertEqual(self.product_3.list_price, 330)
        self.assertEqual(self.product_4.list_price, 400)
        self.assertEqual(self.product_5.list_price, 500)

    def test_06_pricelist_compute_price_formula_round(self):
        self.pricelist_item_by_product.write(
            {
                "compute_price": "formula",
                "price_discount": -10,
                "price_round": 10,
                "price_surcharge": -0.01,
            }
        )
        self.pricelist_item_by_categ.write(
            {
                "compute_price": "formula",
                "price_discount": -20,
                "price_round": 10,
                "price_surcharge": -0.01,
            }
        )
        self.assertEqual(float_compare(self.product_1.list_price, 119.99, 2), 0)
        self.assertEqual(float_compare(self.product_2.list_price, 239.99, 2), 0)
        self.assertEqual(float_compare(self.product_3.list_price, 329.99, 2), 0)
        self.assertEqual(self.product_4.list_price, 400)
        self.assertEqual(self.product_5.list_price, 500)

    def test_06_pricelist_compute_price_formula_cost(self):
        self.pricelist_item_by_product.write(
            {
                "compute_price": "formula",
                "price_discount": -10,
                "base": "standard_price",
            }
        )
        self.pricelist_item_by_categ.write(
            {
                "compute_price": "formula",
                "price_discount": -20,
                "base": "standard_price",
            }
        )
        self.assertEqual(self.product_1.list_price, 96)
        self.assertEqual(self.product_2.list_price, 216)
        self.assertEqual(self.product_3.list_price, 308)
        self.assertEqual(self.product_4.list_price, 400)
        self.assertEqual(self.product_5.list_price, 500)

    def test_06_pricelist_compute_price_formula_other_pricelist(self):
        self.pricelist_item_by_product.write(
            {
                "compute_price": "formula",
                "price_discount": -10,
                "base": "pricelist",
                "base_pricelist_id": self.base_pricelist.id,
            }
        )
        self.pricelist_item_by_categ.write(
            {
                "compute_price": "formula",
                "price_discount": -20,
                "base": "pricelist",
                "base_pricelist_id": self.base_pricelist.id,
            }
        )
        self.assertEqual(self.product_1.list_price, 126)
        self.assertEqual(self.product_2.list_price, 252)
        self.assertEqual(self.product_3.list_price, 363)
        self.assertEqual(self.product_4.list_price, 400)
        self.assertEqual(self.product_5.list_price, 500)

    def test_06_pricelist_compute_price_automatically(self):
        # change fields that trigger recomputation
        self.pricelist_item_by_product.write(
            {
                "compute_price": "formula",
                "price_discount": -10,
                "base": "pricelist",
                "base_pricelist_id": self.base_pricelist.id,
            }
        )
        self.pricelist_item_by_categ.write(
            {
                "compute_price": "formula",
                "price_discount": -20,
                "base": "pricelist",
                "base_pricelist_id": self.base_pricelist.id,
            }
        )
        self.assertEqual(self.product_1.list_price, 126)
        self.assertEqual(self.product_2.list_price, 252)
        self.assertEqual(self.product_3.list_price, 363)
        self.assertEqual(self.product_4.list_price, 400)
        self.assertEqual(self.product_5.list_price, 500)
        # Change fields that do not trigger recomputation
        # the prices should remain unchanged.
        self.pricelist_item_by_product.write(
            {
                "price_max_margin": 100,
                "price_min_margin": 1,
            }
        )
        self.pricelist_item_by_categ.write(
            {
                "price_max_margin": 200,
                "price_min_margin": 2,
            }
        )
        self.assertEqual(self.product_1.list_price, 126)
        self.assertEqual(self.product_2.list_price, 252)
        self.assertEqual(self.product_3.list_price, 363)
        self.assertEqual(self.product_4.list_price, 400)
        self.assertEqual(self.product_5.list_price, 500)

    def test_07_pricelist_global(self):
        """
        product_1 and product_2: Apply a 20% surcharge.
        product_3: Apply a 10% surcharge.
        product_4: Apply a 5% surcharge globally.
        """
        self.pricelist_item_by_categ.write({"percent_price": -20})
        self.pricelist_item_by_product.write({"percent_price": -10})
        self.assertEqual(self.product_1.list_price, 120)
        self.assertEqual(self.product_2.list_price, 240)
        self.assertEqual(self.product_3.list_price, 330)
        self.assertEqual(self.product_4.list_price, 400)  # no rule applied
        self.assertEqual(self.product_5.list_price, 500)  # no rule applied
        # create a new pricelist item global
        # and the all prices should be recomputed automatically for all products
        # according to the rules, but this pricelist triggers the recomputation
        self.PricelistItem.create(
            {
                "pricelist_id": self.pricelist.id,
                "applied_on": "3_global",
                "compute_price": "percentage",
                "percent_price": -5,
            }
        )
        self.assertEqual(self.product_1.list_price, 144)
        self.assertEqual(self.product_2.list_price, 288)
        self.assertEqual(self.product_3.list_price, 363)
        self.assertEqual(self.product_4.list_price, 420)
        self.assertEqual(self.product_5.list_price, 500)

    def test_08_pricelist_min_quantity(self):
        # min_quantity > 1 should not apply the rule
        self.assertEqual(self.product_3.list_price, 300)
        self.pricelist_item_by_product.write({"percent_price": -10, "min_quantity": 2})
        self.assertEqual(self.product_3.list_price, 300)

    def test_08_pricelist_multicompany(self):
        """
        In C1:
        product_1 and product_2: Apply a 20% surcharge.
        product_3: Apply a 10% surcharge.
        product_4: Not affected by the pricelist in C1.
        product_5: Not affected by the pricelist in C1.
        In C2:
        product_1 and product_2: Apply a 5% surcharge.
        product_3: Not affected by the pricelist.
        product_4: Apply a 10% surcharge.
        product_5: Apply a 10% surcharge.
        """
        self.pricelist_item_by_categ.write({"percent_price": -20})
        self.pricelist_item_by_product.write({"percent_price": -10})
        self.assertEqual(self.product_1.list_price, 120)
        self.assertEqual(self.product_2.list_price, 240)
        self.assertEqual(self.product_3.list_price, 330)
        self.assertEqual(self.product_4.list_price, 400)
        self.assertEqual(self.product_5.list_price, 500)
        self.env["ir.config_parameter"].set_param(
            "main_company_compute_price_id", self.company_2.id
        )
        self.pricelist_c2._update_product_price_from_pricelist()
        self.assertEqual(self.product_1.list_price, 126)
        self.assertEqual(self.product_2.list_price, 252)
        self.assertEqual(self.product_3.list_price, 330)
        self.assertEqual(self.product_4.list_price, 440)
        self.assertEqual(self.product_5.list_price, 550)
        # Attempt to compute prices for the pricelist of C1
        # (which does not have a company set, so it uses the environment's company (C2))
        # the prices should remain unchanged.
        self.pricelist.with_company(
            self.company_2
        )._update_product_price_from_pricelist()
        self.assertEqual(self.product_1.list_price, 126)
        self.assertEqual(self.product_2.list_price, 252)
        self.assertEqual(self.product_3.list_price, 330)
        self.assertEqual(self.product_4.list_price, 440)
        self.assertEqual(self.product_5.list_price, 550)
