# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests import TransactionCase


class TestProductTotalWeightFromPackaging(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product = cls.env.ref("product.product_product_20")
        cls.product.weight = 5
        cls.pair_packaging = cls.env["product.packaging"].create(
            {"name": "pair", "product_id": cls.product.id, "qty": 2, "weight": 12.5}
        )
        cls.cardbox_packaging = cls.env["product.packaging"].create(
            {
                "name": "cardbox",
                "product_id": cls.product.id,
                "qty": 10,
                "weight": 55,
            }
        )
        cls.pallet_packaging = cls.env["product.packaging"].create(
            {"name": "pallet", "product_id": cls.product.id, "qty": 200}
        )

    def test_weight_from_packaging(self):
        weight = self.product.get_total_weight_from_packaging(259)
        self.assertEqual(weight, 25 * 55 + 4 * 12.5 + 5)

    def test_weight_in_different_uom(self):
        # Test with product in gram uom
        self.product.product_tmpl_id.write(
            {
                "weight_uom_id": self.env.ref("uom.product_uom_gram").id,
            }
        )
        weight = self.product.get_total_weight_from_packaging(259)
        self.assertEqual(weight, (25 * 55 + 4 * 12.5 + 5) * 1000)

        # Test with 1 packaging in gram uom
        self.pair_packaging.write(
            {
                "weight_uom_id": self.env.ref("uom.product_uom_gram").id,
                "weight": 10000,
            }
        )
        weight = self.product.get_total_weight_from_packaging(259)
        self.assertEqual(weight, (25 * 55 + 5) * 1000 + (4 * 10000))
