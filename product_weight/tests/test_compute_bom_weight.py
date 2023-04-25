# Copyright (C) 2015 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestBomWeightCompute(TransactionCase):
    def setUp(self):
        super().setUp()

        self.ProductModel = self.env["product.product"]

        self.p0 = self.env.ref("product.product_product_25")
        self.p0.write({"weight": 0.00})
        self.p0tmpl = self.env.ref("product.product_product_25_product_template")
        self.p1 = self.env.ref("mrp.product_product_wood_ply")
        self.p1.write({"weight": 0.20})
        self.p1tmpl = self.env.ref("mrp.product_product_wood_ply_product_template")
        self.p2 = self.env.ref("mrp.product_product_computer_desk_screw")
        self.p2.write({"weight": 0.22})
        self.p2tmpl = self.env.ref(
            "mrp.product_product_computer_desk_screw_product_template"
        )
        self.p3 = self.env.ref("mrp.product_product_wood_wear")
        self.p3.write({"weight": 0.68})
        self.p3tmpl = self.env.ref("mrp.product_product_wood_wear_product_template")
        self.p4 = self.env.ref("mrp.product_product_ply_veneer")
        self.p4.write({"weight": 0.10})
        self.p4tmpl = self.env.ref("mrp.product_product_ply_veneer_product_template")
        self.v1 = self.env.ref("product.product_product_20")
        self.v1.write({"weight": 0.00})
        self.v1tmpl = self.env.ref("product.product_product_20_product_template")
        self.v2 = self.env.ref("mrp.product_product_computer_desk_leg")
        self.v2.write({"weight": 0.00})
        self.v2tmpl = self.env.ref(
            "mrp.product_product_computer_desk_leg_product_template"
        )

        self.BomModel = self.env["mrp.bom"]
        self.bom = self.BomModel.create(
            {
                "product_tmpl_id": self.p0tmpl.id,
                "product_id": self.p0.id,
                "product_qty": 1,
                "type": "normal",
            }
        )
        self.bom1 = self.BomModel.create(
            {
                "product_tmpl_id": self.p1tmpl.id,
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
            active_model="product.template", active_id=self.p0tmpl.id
        ).create({})
        wizard.update_single_weight()
        self.assertAlmostEqual(self.p0.weight, 4)
        self.assertAlmostEqual(self.p0tmpl.weight, 4)

    def test_calculate_product_weight_from_product_form(self):
        wizard = self.WizObj.with_context(
            active_model="product.product", active_id=self.p0.id
        ).create({})
        wizard.update_single_weight()
        self.assertAlmostEqual(self.p0.weight, 4)
        self.assertAlmostEqual(self.p0tmpl.weight, 4)

    def test_calculate_weight_from_template_tree(self):
        self.bom.product_tmpl_id = self.v1tmpl.id
        self.bom.product_id = self.v1.id
        wizard = self.WizObj.with_context(
            active_model="product.template",
            active_ids=[self.v1tmpl.id, self.v2tmpl.id],
        ).create({})
        wizard.update_multi_product_weight()
        # You can't update template weight if it as variants
        self.assertAlmostEqual(self.v1tmpl.weight, 4)
        self.assertAlmostEqual(self.v2tmpl.weight, 0.0)

    def test_calculate_weight_from_product_tree(self):
        self.bom.product_tmpl_id = self.v1tmpl.id
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
            active_model="product.template", active_id=self.p0tmpl.id
        ).create({})
        wizard.update_single_weight()
        self.assertAlmostEqual(self.p0.weight, 0.34)
        self.assertAlmostEqual(self.p0tmpl.weight, 0.34)

    def test_bom_different_qty(self):
        self.bom.product_qty = self.bom.product_qty * 2
        for bomline in self.bom.bom_line_ids:
            bomline.product_qty = bomline.product_qty * 2
        wizard = self.WizObj.with_context(
            active_model="product.template", active_id=self.p0tmpl.id
        ).create({})
        wizard.update_single_weight()
        self.assertAlmostEqual(self.p0tmpl.weight, 4)
        self.assertAlmostEqual(self.p0.weight, 4)

    def test_cron_weight_update(self):
        self.p2.write({"weight": 0.44})
        self.p3.write({"weight": 0.85})
        self.p4.write({"weight": 0.20})
        self.ProductModel.cron_recompute_bom_weight()
        self.assertAlmostEqual(self.p0.weight, 5.96)
        self.assertAlmostEqual(self.p0tmpl.weight, 5.96)
        self.assertAlmostEqual(self.p1.weight, 0.40)
        self.assertAlmostEqual(self.p1tmpl.weight, 0.40)
