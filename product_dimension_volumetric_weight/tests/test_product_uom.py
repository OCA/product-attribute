# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo.tests.common import Form


class TestProductUom(common.SavepointCase):
    def setUp(self):
        super().setUp()
        self.uom_m = self.env.ref("uom.product_uom_meter")
        self.uom_m.write({"volumetric_weight_ratio": 400})
        self.uom_cm = self.env.ref("uom.product_uom_cm")
        self.uom_cm.write({"volumetric_weight_ratio": 400})

    def test_volumetric_weight_in_m(self):
        product_form = Form(self.env["product.template"])
        product_form.name = "Test product"
        product_form.dimensional_uom_id = self.uom_m
        product_form.volume = 1
        self.assertAlmostEqual(400, product_form.volumetric_weight)

    def test_volumetric_weight_in_cm(self):
        product_form = Form(self.env["product.template"])
        product_form.name = "Test product"
        product_form.dimensional_uom_id = self.uom_cm
        product_form.volume = 0.12
        self.assertAlmostEqual(48, product_form.volumetric_weight)
