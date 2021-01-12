# Copyright (C) 2015 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestBomWeightCompute(TransactionCase):
    def setUp(self):
        super().setUp()
        self.ProductModel = self.env["product.product"]
        unit_uom_id = self.env.ref("uom.product_uom_unit").id
        self.p0 = self.ProductModel.create({"name": "000", "type": "product"})
        self.p1 = self.ProductModel.create(
            {"name": "101", "type": "product", "weight": 0.20, "uom_id": unit_uom_id}
        )
        self.p2 = self.ProductModel.create(
            {"name": "202", "type": "product", "weight": 0.22, "uom_id": unit_uom_id}
        )
        self.p3 = self.ProductModel.create(
            {"name": "303", "type": "product", "weight": 0.68, "uom_id": unit_uom_id}
        )
        self.p4 = self.ProductModel.create(
            {"name": "404", "type": "product", "weight": 0.10, "uom_id": unit_uom_id}
        )
        self.v1 = self.ProductModel.create(
            {"name": "v101", "type": "product", "weight": 0.00, "uom_id": unit_uom_id}
        )
        self.v2 = self.ProductModel.create(
            {"name": "v202", "type": "product", "weight": 0.00, "uom_id": unit_uom_id}
        )
        self.BomModel = self.env["mrp.bom"]
        self.bom = self.BomModel.create(
            {
                "product_tmpl_id": self.p0.product_tmpl_id.id,
                "product_id": self.p0.id,
                "product_qty": 1,
                "type": "normal",
            }
        )
        self.bom1 = self.BomModel.create(
            {
                "product_tmpl_id": self.p1.product_tmpl_id.id,
                "product_id": self.p1.id,
                "product_qty": 1,
                "type": "phantom",
            }
        )
        # Create bom lines
        self.BomLine = self.env["mrp.bom.line"]
        self.BomLine.create(
            {"bom_id": self.bom.id, "product_id": self.p1.id, "product_qty": 2}
        )
        self.BomLine.create(
            {"bom_id": self.bom.id, "product_id": self.p2.id, "product_qty": 4}
        )
        self.BomLine.create(
            {"bom_id": self.bom.id, "product_id": self.p3.id, "product_qty": 4}
        )
        self.BomLine.create(
            {"bom_id": self.bom1.id, "product_id": self.p4.id, "product_qty": 2}
        )
        self.WizObj = self.env["product.weight.update"]

    def test_calculate_product_weight_from_template_form(self):
        wizard = self.WizObj.with_context(
            active_model="product.template", active_id=self.p0.product_tmpl_id.id
        ).create({})
        wizard.update_single_weight()
        self.assertAlmostEqual(self.p0.weight, 4)
        self.assertAlmostEqual(self.p0.product_tmpl_id.weight, 4)

    def test_calculate_product_weight_from_product_form(self):
        wizard = self.WizObj.with_context(
            active_model="product.product", active_id=self.p0.id
        ).create({})
        wizard.update_single_weight()
        self.assertAlmostEqual(self.p0.weight, 4)
        self.assertAlmostEqual(self.p0.product_tmpl_id.weight, 4)

    def test_calculate_weight_from_template_tree(self):
        self.bom.product_tmpl_id = self.v1.product_tmpl_id.id
        self.bom.product_id = self.v1.id
        wizard = self.WizObj.with_context(
            active_model="product.template",
            active_ids=[self.v1.product_tmpl_id.id, self.v2.product_tmpl_id.id],
        ).create({})
        wizard.update_multi_product_weight()
        # You can't update template weight if it as variants
        self.assertAlmostEqual(self.v1.product_tmpl_id.weight, 4)
        self.assertAlmostEqual(self.v2.product_tmpl_id.weight, 0.0)

    def test_calculate_weight_from_product_tree(self):
        self.bom.product_tmpl_id = self.v1.product_tmpl_id.id
        self.bom.product_id = self.v1.id
        wizard = self.WizObj.with_context(
            active_model="product.product", active_ids=[self.v1.id, self.v2.id]
        ).create({})
        wizard.update_multi_product_weight()
        self.assertAlmostEqual(self.v1.weight, 4)
        self.assertAlmostEqual(self.v2.weight, 0.0)

    def test_empty_fields(self):
        res = self.WizObj.default_get([])
        self.assertEqual(res, {})

    def test_weight_bom_different_uom(self):
        dozen_uom_id = self.env.ref("uom.product_uom_dozen").id
        self.bom.product_uom_id = dozen_uom_id
        wizard = self.WizObj.with_context(
            active_model="product.template", active_id=self.p0.product_tmpl_id.id
        ).create({})
        wizard.update_single_weight()
        self.assertAlmostEqual(self.p0.weight, 0.34)
        self.assertAlmostEqual(self.p0.product_tmpl_id.weight, 0.34)

    def test_bom_different_qty(self):
        self.bom.product_qty = self.bom.product_qty * 2
        for bomline in self.bom.bom_line_ids:
            bomline.product_qty = bomline.product_qty * 2
        wizard = self.WizObj.with_context(
            active_model="product.template", active_id=self.p0.product_tmpl_id.id
        ).create({})
        wizard.update_single_weight()
        self.assertAlmostEqual(self.p0.weight, 4)
        self.assertAlmostEqual(self.p0.product_tmpl_id.weight, 4)
