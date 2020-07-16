# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests import SavepointCase


class TestProductTotalWeightFromPackaging(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product = cls.env.ref("product.product_product_20")
        cls.product.weight = 5
        cls.env["product.packaging"].create(
            {"name": "pair", "product_id": cls.product.id, "qty": 2, "max_weight": 12.5}
        )
        cls.env["product.packaging"].create(
            {
                "name": "cardbox",
                "product_id": cls.product.id,
                "qty": 10,
                "max_weight": 55,
            }
        )
        cls.env["product.packaging"].create(
            {"name": "pallet", "product_id": cls.product.id, "qty": 200}
        )

    def test_weight_from_packaging(self):
        weight = self.product.get_total_weight_from_packaging(259)
        self.assertEqual(weight, 25 * 55 + 4 * 12.5 + 5)
