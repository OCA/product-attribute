# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from psycopg2 import IntegrityError

from odoo.tests.common import TransactionCase
from odoo.tools.misc import mute_logger


class TestUomQtyUnique(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.unit = cls.env.ref("uom.product_uom_unit")
        cls.uom_dozen = cls.env.ref("uom.product_uom_dozen")
        cls.uom_dozen.active = True

    @mute_logger("odoo.sql_db")
    def test_uom_qty_unique(self):
        # Create a duplicate unit of measure
        with self.assertRaises(IntegrityError):
            self.env["uom.uom"].create(
                {
                    "name": "Dozen",
                    "relative_factor": 12.0,
                    "relative_uom_id": self.unit.id,
                }
            )

    def test_uom_qty_unique_archived(self):
        # Archive the dozen unit of measure
        self.uom_dozen.active = False
        self.env["uom.uom"].create(
            {
                "name": "Dozen",
                "relative_factor": 12.0,
                "relative_uom_id": self.unit.id,
            }
        )
