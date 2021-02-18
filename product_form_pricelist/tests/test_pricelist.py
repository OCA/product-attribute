# Copyright 2021 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests import SavepointCase


class TestPricelist(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tmpl = cls.env["product.template"].create({"name": "Foo"})
        cls.variant = cls.tmpl.product_variant_ids

    def test_write_pricelist_item(self):
        price = self.env["product.pricelist.item"].create(
            {
                "product_tmpl_id": self.tmpl.id,
                "fixed_price": 100,
                "applied_on": "1_product",
            }
        )
        price.product_id = self.tmpl.product_variant_ids.id
        self.assertEqual(price.applied_on, "0_product_variant")

    def test_create_pricelist_item(self):
        tmpl = self.env["product.template"].create({"name": "Foo"})
        price = self.env["product.pricelist.item"].create(
            {
                "product_tmpl_id": tmpl.id,
                "fixed_price": 100,
            }
        )
        self.assertEqual(price.applied_on, "1_product")

    def test_create_variant_pricelist_item(self):
        price = self.env["product.pricelist.item"].create(
            {
                "product_id": self.variant.id,
                "fixed_price": 100,
            }
        )
        self.assertEqual(price.applied_on, "0_product_variant")
        self.assertEqual(price.product_tmpl_id, self.tmpl)

    def test_write_variant_pricelist_item(self):
        price = self.env["product.pricelist.item"].create(
            {
                "product_id": self.variant.id,
                "fixed_price": 100,
            }
        )
        tmpl = self.env["product.template"].create({"name": "Foo"})
        variant = tmpl.product_variant_ids.id
        price.product_id = variant
        self.assertEqual(price.applied_on, "0_product_variant")
        self.assertEqual(price.product_tmpl_id, tmpl)
