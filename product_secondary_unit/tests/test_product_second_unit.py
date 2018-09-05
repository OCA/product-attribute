# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import SavepointCase


class TestProductSecondaryUnit(SavepointCase):
    at_install = False
    post_install = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_uom_kg = cls.env.ref('product.product_uom_kgm')
        cls.product_uom_unit = cls.env.ref('product.product_uom_unit')
        cls.product = cls.env['product.template'].create({
            'name': 'test',
            'uom_id': cls.product_uom_kg.id,
            'uom_po_id': cls.product_uom_kg.id,
            'secondary_uom_ids': [
                (0, 0, {
                    'name': 'unit-700',
                    'uom_id': cls.product_uom_unit.id,
                    'factor': 0.7,
                })],
        })
        secondary_unit = cls.env['product.secondary.unit'].search([
            ('product_tmpl_id', '=', cls.product.id),
        ])
        cls.product.sale_secondary_uom_id = secondary_unit.id

    def test_product_secondary_unit_name(self):
        self.assertEqual(
            self.product.sale_secondary_uom_id.name_get()[0][1], 'Unit(s)-0.7')
