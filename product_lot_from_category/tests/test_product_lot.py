# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import Form
from odoo.tests.common import SavepointCase


class TestProductAssortment(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_obj = cls.env["product.template"]
        cls.categ_obj = cls.env["product.category"]
        cls.product = cls.env.ref("product.product_product_4").product_tmpl_id

        vals = {
            "name": "Category Lot",
            "tracking": "lot",
        }
        cls.category = cls.categ_obj.create(vals)

    def test_product_lot_values(self):
        with Form(self.product) as product_form:
            product_form.categ_id = self.category
        self.assertEqual(
            self.product.tracking,
            "lot",
        )

    def test_product_variant_lot_values(self):
        variant = self.product.product_variant_ids[0]
        with Form(variant) as product_form:
            product_form.categ_id = self.category
        self.assertEqual(
            variant.tracking,
            "lot",
        )
