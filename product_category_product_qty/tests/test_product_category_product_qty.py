# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestProductCategory(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.category_model = cls.env["product.category"]
        cls.product_corner_desk = cls.env.ref("product.product_product_5")

    def test_compute_product_variant_count(self):
        # Create some product categories
        category1 = self.category_model.create({"name": "Category 1"})

        # Check computed value
        category1._compute_product_variant_count()
        self.assertEqual(category1.product_variant_count, 0)

        # Change categories
        self.product_corner_desk.write(
            {
                "categ_id": category1.id,
            }
        )

        # Check computed value
        category1._compute_product_variant_count()
        self.assertEqual(category1.product_variant_count, 1)
