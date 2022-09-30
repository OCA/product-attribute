# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from psycopg2 import IntegrityError

from odoo.tests.common import SavepointCase
from odoo.tools.misc import mute_logger


class TestUomQtyUnique(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.unit = cls.env.ref("uom.product_uom_categ_unit")

    @mute_logger("odoo.sql_db")
    def test_uom_qty_unique(self):
        # Create a duplicate unit of measure
        with self.assertRaises(IntegrityError):
            self.env["uom.uom"].create(
                {
                    "name": "Dozen",
                    "factor_inv": 12.0,
                    "uom_type": "bigger",
                    "category_id": self.unit.id,
                }
            )

    def test_uom_qty_unique_archived(self):
        # Archive the dozen unit of measure
        uom_dozen = self.env.ref("uom.product_uom_dozen")
        uom_dozen.active = False
        self.env["uom.uom"].create(
            {
                "name": "Dozen",
                "factor_inv": 12.0,
                "uom_type": "bigger",
                "category_id": self.unit.id,
            }
        )
