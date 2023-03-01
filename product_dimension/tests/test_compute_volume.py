# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestComputeVolumeOnProduct(TransactionCase):
    def test_it_computes_volume_in_cm_using_meter(self):
        self.env['ir.config_parameter'].sudo().set_param('product.volume_in_cubic_feet', '0')
        self.product.product_length = 10.0
        self.product.product_height = 200.0
        self.product.product_width = 100.0
        self.product.dimensional_uom_id = self.uom_cm
        self.product.onchange_calculate_volume()
        self.assertAlmostEqual(0.2, self.product.volume)

    def test_it_computes_volume_in_meters_using_meter(self):
        self.env['ir.config_parameter'].sudo().set_param('product.volume_in_cubic_feet', '0')
        self.product.product_length = 6.0
        self.product.product_height = 2.0
        self.product.product_width = 10.0
        self.product.dimensional_uom_id = self.uom_m
        self.product.onchange_calculate_volume()
        self.assertAlmostEqual(120, self.product.volume)

    def test_it_computes_volume_in_in_using_foot(self):
        self.env['ir.config_parameter'].sudo().set_param('product.volume_in_cubic_feet', '1')
        self.product.product_length = 12.0
        self.product.product_height = 144.0
        self.product.product_width = 120.0
        self.product.dimensional_uom_id = self.uom_in
        self.product.onchange_calculate_volume()
        self.assertAlmostEqual(120, self.product.volume)

    def test_it_computes_volume_in_feet_using_foot(self):
        self.env['ir.config_parameter'].sudo().set_param('product.volume_in_cubic_feet', '1')
        self.product.product_length = 6.0
        self.product.product_height = 2.0
        self.product.product_width = 10.0
        self.product.dimensional_uom_id = self.uom_ft
        self.product.onchange_calculate_volume()
        self.assertAlmostEqual(120, self.product.volume)

    def setUp(self):
        super(TestComputeVolumeOnProduct, self).setUp()

        self.product = self.env["product.product"].new()
        self.uom_m = self.env["uom.uom"].search([("name", "=", "m")])
        self.uom_cm = self.env["uom.uom"].search([("name", "=", "cm")])
        self.uom_ft = self.env["uom.uom"].search([("name", "=", "ft")])
        self.uom_in = self.env["uom.uom"].search([("name", "=", "in")])


class TestComputeVolumeOnTemplate(TransactionCase):
    def test_it_computes_volume_in_cm(self):
        self.template.product_length = 10.0
        self.template.product_height = 200.0
        self.template.product_width = 100.0
        self.template.dimensional_uom_id = self.uom_cm
        self.template.onchange_calculate_volume()
        self.assertAlmostEqual(0.2, self.template.volume)

    def test_it_computes_volume_in_meters(self):
        self.template.product_length = 6.0
        self.template.product_height = 2.0
        self.template.product_width = 10.0
        self.template.dimensional_uom_id = self.uom_m
        self.template.onchange_calculate_volume()
        self.assertAlmostEqual(120, self.template.volume)

    def setUp(self):
        super(TestComputeVolumeOnTemplate, self).setUp()

        self.template = self.env["product.template"].new()
        self.uom_m = self.env["uom.uom"].search([("name", "=", "m")])
        self.uom_cm = self.env["uom.uom"].search([("name", "=", "cm")])
