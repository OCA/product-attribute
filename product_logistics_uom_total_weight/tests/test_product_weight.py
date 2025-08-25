# Copyright 2024 (APSL-Nagarro) - Miquel Alzanillas, Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests.common import TransactionCase


class TestProductWeight(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product = cls.env.ref("product.product_product_6")
        cls.product2 = cls.env["product.product"].create(
            {
                "name": "Test",
                "uom_id": cls.env.ref("uom.product_uom_gram").id,
                "uom_po_id": cls.env.ref("uom.product_uom_gram").id,
                "detailed_type": "product",
            }
        )
        cls.product_template = cls.env.ref("product.product_product_7_product_template")
        cls.product_template2 = cls.env["product.template"].create(
            {
                "name": "Test",
                "uom_id": cls.env.ref("uom.product_uom_gram").id,
                "uom_po_id": cls.env.ref("uom.product_uom_gram").id,
                "detailed_type": "product",
            }
        )

    def test_product_total_weight(self):
        self.product.qty_available = 20
        total_weight = self.product.qty_available * self.product.product_weight
        self.assertEqual(self.product.total_weight, total_weight)
        self.product_template.qty_available = 20
        total_weight = (
            self.product_template.qty_available * self.product_template.product_weight
        )
        self.assertEqual(self.product_template.total_weight, total_weight)
        self.product2.qty_available = 20
        total_weight = (
            self.product2.qty_available * self.product2.product_weight
        ) / self.product2.weight_uom_id.factor
        self.assertEqual(self.product2.total_weight, total_weight)
        self.product_template2.qty_available = 20
        total_weight = (
            self.product_template2.qty_available * self.product_template2.product_weight
        ) / self.product_template2.weight_uom_id.factor
        self.assertEqual(self.product_template2.total_weight, total_weight)
