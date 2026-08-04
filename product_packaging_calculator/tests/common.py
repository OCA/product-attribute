# Copyright 2020 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
from odoo.addons.base.tests.common import BaseCommon


class TestCommon(BaseCommon):
    at_install = False
    post_install = True
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product_a = cls.env["product.product"].create(
            {
                "name": "Product A",
                "uom_id": cls.uom_unit.id,
            }
        )
        cls.pkg_box = cls._create_packaging("Box", 50, "BOX")
        cls.pkg_big_box = cls._create_packaging("Big Box", 200, "BIGBOX")
        cls.pkg_pallet = cls._create_packaging("Pallet", 2000, "PALLET")

    @classmethod
    def _create_packaging(cls, name, qty, barcode):
        """Create a packaging as a UoM linked to product_a with a barcode."""
        uom = cls.env["uom.uom"].create(
            {
                "name": name,
                "relative_uom_id": cls.uom_unit.id,
                "relative_factor": qty,
            }
        )
        cls.product_a.uom_ids = [(4, uom.id)]
        cls.env["product.uom"].create(
            {
                "product_id": cls.product_a.id,
                "uom_id": uom.id,
                "barcode": barcode,
            }
        )
        return uom
