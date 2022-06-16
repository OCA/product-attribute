# SPDX-FileCopyrightText: 2022 Coop IT Easy SCRLfs
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo.tests.common import SavepointCase


class TestComputeVolumeOnProduct(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.product = cls.env["product.product"].create({"name": "Product"})
        cls.uom_m = cls.env["uom.uom"].search([("name", "=", "m")])
        cls.uom_cm = cls.env["uom.uom"].search([("name", "=", "cm")])
        cls.uom_litre = cls.env.ref("uom.product_uom_litre")

    def test_compute_in_cm(self):
        self.assertAlmostEqual(self.product.volume, 0)

        self.product.product_length = 10
        self.product.product_height = 200
        self.product.product_width = 100
        self.product.dimensional_uom_id = self.uom_cm
        self.product.volume_uom_id = self.uom_litre
        self.assertAlmostEqual(self.product.volume, 200)

        self.product.product_length = 0
        self.assertAlmostEqual(self.product.volume, 0)

    def test_compute_in_m(self):
        self.product.product_length = 6
        self.product.product_height = 2
        self.product.product_width = 10
        self.product.dimensional_uom_id = self.uom_m
        self.product.volume_uom_id = self.uom_litre
        self.assertAlmostEqual(self.product.volume, 120000)


class TestComputeVolumeOnTemplate(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.template = cls.env["product.template"].create({"name": "Template"})
        cls.uom_m = cls.env["uom.uom"].search([("name", "=", "m")])
        cls.uom_cm = cls.env["uom.uom"].search([("name", "=", "cm")])
        cls.uom_litre = cls.env.ref("uom.product_uom_litre")

    def test_compute_in_cm(self):
        self.assertAlmostEqual(self.template.volume, 0)

        self.template.product_length = 10
        self.template.product_height = 200
        self.template.product_width = 100
        self.template.dimensional_uom_id = self.uom_cm
        self.template.volume_uom_id = self.uom_litre
        self.assertAlmostEqual(self.template.volume, 200)

        self.template.product_length = 0
        self.assertAlmostEqual(self.template.volume, 0)

    def test_compute_in_m(self):
        self.template.product_length = 6
        self.template.product_height = 2
        self.template.product_width = 10
        self.template.dimensional_uom_id = self.uom_m
        self.template.volume_uom_id = self.uom_litre
        self.assertAlmostEqual(self.template.volume, 120000)
