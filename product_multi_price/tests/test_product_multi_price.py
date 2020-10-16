# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import SavepointCase


class TestProductMultiPrice(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.price_name_obj = cls.env["product.multi.price.name"]
        cls.price_field_1 = cls.price_name_obj.create({"name": "test_field_1"})
        cls.price_field_2 = cls.price_name_obj.create({"name": "test_field_2"})
        prod_tmpl_obj = cls.env["product.template"]
        cls.prod_1 = prod_tmpl_obj.create(
            {
                "name": "Test Product Template",
                "price_ids": [
                    (0, 0, {"name": cls.price_field_1.id, "price": 5.5}),
                    (0, 0, {"name": cls.price_field_2.id, "price": 20.0}),
                ],
            }
        )
        cls.prod_att_1 = cls.env["product.attribute"].create({"name": "Color"})
        cls.prod_attr1_v1 = cls.env["product.attribute.value"].create(
            {"name": "red", "attribute_id": cls.prod_att_1.id}
        )
        cls.prod_attr1_v2 = cls.env["product.attribute.value"].create(
            {"name": "blue", "attribute_id": cls.prod_att_1.id}
        )
        cls.prod_2 = prod_tmpl_obj.create(
            {
                "name": "Test Product 2 With Variants",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.prod_att_1.id,
                            "value_ids": [
                                (6, 0, [cls.prod_attr1_v1.id, cls.prod_attr1_v2.id])
                            ],
                        },
                    )
                ],
            }
        )
        cls.prod_prod_2_1 = cls.prod_2.product_variant_ids[0]
        cls.prod_prod_2_2 = cls.prod_2.product_variant_ids[1]
        cls.prod_prod_2_1.write(
            {
                "price_ids": [
                    (0, 0, {"name": cls.price_field_1.id, "price": 6.6}),
                    (0, 0, {"name": cls.price_field_2.id, "price": 7.7}),
                ],
            }
        )
        cls.prod_prod_2_2.write(
            {
                "price_ids": [
                    (0, 0, {"name": cls.price_field_1.id, "price": 8.8}),
                    (0, 0, {"name": cls.price_field_2.id, "price": 9.9}),
                ],
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test pricelist",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "compute_price": "formula",
                            "base": "multi_price",
                            "multi_price_name": cls.price_field_1.id,
                            "price_discount": 10,
                            "applied_on": "3_global",
                        },
                    )
                ],
            }
        )

    def test_product_multi_price_pricelist(self):
        """Pricelists based on multi prices for templates or variants"""
        price = self.prod_1.with_context(pricelist=self.pricelist.id).price
        self.assertAlmostEqual(price, 4.95)
        price = self.prod_prod_2_1.with_context(pricelist=self.pricelist.id).price
        self.assertAlmostEqual(price, 5.94)
        price = self.prod_prod_2_2.with_context(pricelist=self.pricelist.id).price
        self.assertAlmostEqual(price, 7.92)
