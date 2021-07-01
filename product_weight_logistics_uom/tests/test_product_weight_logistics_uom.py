# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestBomWeightCompute(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Wiz = self.env["product.weight.update"]
        self.Product = self.env["product.product"]
        self.Bom = self.env["mrp.bom"]
        self.BomLine = self.env["mrp.bom.line"]
        kg_uom = self.env.ref("uom.product_uom_kgm").id
        g_uom = self.env.ref("uom.product_uom_gram").id
        self.a = self.Product.create(
            {
                "name": "raw a in kg",
                "type": "product",
                "weight": 1.2,
                "weight_uom_id": kg_uom,
            }
        )
        self.b = self.Product.create(
            {
                "name": "raw b in g",
                "type": "product",
                "weight": 150,
                "weight_uom_id": g_uom,
            }
        )
        self.fnkg = self.Product.create(
            {
                "name": "fin in kg",
                "type": "product",
                "weight": 0,
                "weight_uom_id": kg_uom,
            }
        )
        self.fng = self.Product.create(
            {"name": "fin in g", "type": "product", "weight": 0, "weight_uom_id": g_uom}
        )

        self.bomkg = self.Bom.create(
            {
                "product_tmpl_id": self.fnkg.product_tmpl_id.id,
                "product_id": self.fnkg.id,
                "product_qty": 1,
                "type": "normal",
            }
        )
        self.bomg = self.Bom.create(
            {
                "product_tmpl_id": self.fng.product_tmpl_id.id,
                "product_id": self.fng.id,
                "product_qty": 1,
                "type": "normal",
            }
        )
        # Create bom lines
        self.qta = 1
        self.qtb = 1
        self.BomLine.create(
            {"bom_id": self.bomkg.id, "product_id": self.a.id, "product_qty": self.qta}
        )
        self.BomLine.create(
            {"bom_id": self.bomkg.id, "product_id": self.b.id, "product_qty": self.qtb}
        )
        self.BomLine.create(
            {"bom_id": self.bomg.id, "product_id": self.a.id, "product_qty": self.qta}
        )
        self.BomLine.create(
            {"bom_id": self.bomg.id, "product_id": self.b.id, "product_qty": self.qtb}
        )

    def test_calculate_product_weight_from_template_form(self):
        expected_in_g = self.a.weight * self.qta * 1000 + self.b.weight * self.qtb
        expected_in_kg = expected_in_g / 1000
        wizard = self.Wiz.with_context(
            active_model="product.template", active_id=self.fnkg.product_tmpl_id.id
        ).create({})
        wizard.update_single_weight()
        self.assertAlmostEqual(self.fnkg.weight, expected_in_kg)

        wizard = self.Wiz.with_context(
            active_model="product.template", active_id=self.fng.product_tmpl_id.id
        ).create({})
        wizard.update_single_weight()
        self.assertAlmostEqual(self.fng.weight, expected_in_g)
