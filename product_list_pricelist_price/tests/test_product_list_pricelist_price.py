# Copyright 2021 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProductListPricelistPrice(TransactionCase):
    def setUp(self):
        super(TestProductListPricelistPrice, self).setUp()
        # Required models
        self.product_template_model = self.env["product.template"]
        self.product_variant_model = self.env["product.product"]
        self.pricelist_model = self.env["product.pricelist"]
        # Create product
        self.product_template = self.product_template_model.create(
            {"name": "Test Product"}
        )
        self.product_variant = self.product_template.product_variant_ids[0]
        # Get system pricelists and mark only one to be displayed
        self.pricelists = self.pricelist_model.search([])
        self.displayed_pricelist = self.pricelists[0]
        self.displayed_pricelist.write({"display_pricelist_price": True})

    def test_registry_hook(self):
        self.product_variant_model._register_hook()
        self.product_template_model._register_hook()
        for pricelist in self.pricelists:
            template_field_name = "product_tmpl_price_pricelist_%s" % (pricelist.id)
            variant_field_name = "product_price_pricelist_%s" % (pricelist.id)
            if pricelist == self.displayed_pricelist:
                self.assertTrue(self.product_template[template_field_name])
                self.assertTrue(self.product_variant[variant_field_name])
            else:
                with self.assertRaises(KeyError):
                    self.assertTrue(self.product_template[template_field_name])
                    self.assertTrue(self.product_variant[variant_field_name])
