# Copyright 2018-2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import psycopg2

from odoo.tests.common import SavepointCase
from odoo.tools.misc import mute_logger


class TestProductstate(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_obj = cls.env["product.state"]
        cls.product1 = cls.product_obj.create({"name": "Test Code 1", "code": "TSTP1"})

    def test_01_check_code_other(self):
        self.product2 = self.product_obj.create(
            {"name": "Test Code 2", "code": "TSTP2"}
        )

    def test_02_check_code_state(self):
        with self.assertRaises(psycopg2.IntegrityError):
            with mute_logger("odoo.sql_db"), self.cr.savepoint():
                self.product2 = self.product_obj.create(
                    {"name": "Test Code 2", "code": "TSTP1"}
                )
