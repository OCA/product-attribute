# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestProductRouteMto(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.route_mto = cls.env.ref("stock.route_warehouse0_mto")
        cls.route_mto.active = True
        cls.route_mto.product_categ_selectable = True
        cls.route_mto.product_selectable = True
        cls.category = cls.env["product.category"].create({"name": "Test Category"})
        cls.product = cls.env["product.template"].create(
            {
                "name": "Product Test",
                "categ_id": cls.category.id,
            }
        )

    def test_product_route(self):
        self.assertFalse(self.product.is_mto)
        self.product.route_ids += self.route_mto
        self.assertTrue(self.product.is_mto)

    def test_category_route(self):
        self.assertFalse(self.product.is_mto)
        self.product.categ_id.write({"route_ids": [(4, self.route_mto.id)]})
        self.env.flush_all()
        self.assertTrue(self.product.is_mto)
