# Copyright (C) 2025  Renato Lima - Akretion
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestUomAlias(TransactionCase):
    def setUp(self):
        super().setUp()
        self.uom_unit = self.env.ref("uom.product_uom_unit")
        self.uom_unit.write(
            {
                "alias_ids": [
                    (0, 0, {"code": "XXX"}),
                    (0, 0, {"code": "YYY"}),
                    (0, 0, {"code": "ZZZ"}),
                ]
            }
        )

    def test_search(self):
        """Testing search method with alias"""
        # Test search with alias "XXX"
        uom = self.env["uom.uom"].search([("name", "=", "XXX")])
        self.assertEqual(uom, self.uom_unit)

        # Test search with alias "YYY"
        uom = self.env["uom.uom"].search([("name", "=", "YYY")])
        self.assertEqual(uom, self.uom_unit)

        # Test search with alias "ZZZ"
        uom = self.env["uom.uom"].search([("name", "=", "ZZZ")])
        self.assertEqual(uom, self.uom_unit)

    def test_name_search(self):
        """Testing name_search method with alias"""
        # Test name_search with alias "XXX"
        uom = self.env["uom.uom"].name_search("XXX")
        self.assertTrue(uom)

        # Test name_search with alias "YYY"
        uom = self.env["uom.uom"].name_search("YYY")
        self.assertTrue(uom)

        # Test name_search with alias "ZZZ"
        uom = self.env["uom.uom"].name_search("ZZZ")
        self.assertTrue(uom)
