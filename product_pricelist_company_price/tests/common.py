#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase


class Common(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product",
                "lst_price": 100,
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Pricelist",
            }
        )
        cls.company.products_price_pricelist_id = cls.pricelist

    def _create_item(self, pricelist, product, price):
        item_values = {
            "pricelist_id": pricelist.id,
            "compute_price": "fixed",
            "fixed_price": price,
        }
        if product._name == "product.product":
            item_values.update(
                {
                    "applied_on": "0_product_variant",
                    "product_id": product.id,
                }
            )
        elif product._name == "product.template":
            item_values.update(
                {
                    "applied_on": "1_product",
                    "product_tmpl_id": product.id,
                }
            )
        item = self.env["product.pricelist.item"].create(item_values)
        return item
