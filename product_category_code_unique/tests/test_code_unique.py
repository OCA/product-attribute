# Copyright 2021 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from psycopg2 import IntegrityError

import odoo.tests.common as common
from odoo.tools import mute_logger


class TestProductCode(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        vals = {
            "name": "Category Test",
            "code": "TEST",
        }
        cls.category = cls.env["product.category"].create(vals)

    @mute_logger("odoo.sql_db")
    def test_category_code_unique(self):
        vals = {
            "name": "Category Test duplicate",
            "code": "TEST",
        }
        with self.assertRaises(IntegrityError), self.env.cr.savepoint():
            self.env["product.category"].create(vals)

        vals.update({"code": "TEST1"})
        self.env["product.category"].create(vals)

        vals = {
            "name": "Category Auto",
        }
        self.category_2 = self.env["product.category"].create(vals)
        self.assertIn(
            "PC/",
            self.category_2.code,
        )
