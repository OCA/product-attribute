# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo.tests import tagged

from odoo.addons.product.tests.common import ProductCommon


# `account` is loaded after this module, hence its `res.partner` columns are
# not in the registry yet when tests run at install.
@tagged("post_install", "-at_install")
class TestProductTotalWeightFromPackaging(ProductCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls._create_product(weight=5)
        cls.pair_uom = cls._create_packaging_uom("pair", 2)
        cls.cardbox_uom = cls._create_packaging_uom("cardbox", 10)
        cls.pallet_uom = cls._create_packaging_uom("pallet", 200)
        cls.pair_packaging = cls._create_packaging(cls.pair_uom, 12.5)
        cls.cardbox_packaging = cls._create_packaging(cls.cardbox_uom, 55)
        # No weight, hence ignored by the estimation
        cls.pallet_packaging = cls._create_packaging(cls.pallet_uom, 0)

    @classmethod
    def _create_packaging_uom(cls, name, factor):
        return cls.env["uom.uom"].create(
            {
                "name": name,
                "relative_factor": factor,
                "relative_uom_id": cls.uom_unit.id,
            }
        )

    @classmethod
    def _create_packaging(cls, uom, weight):
        return cls.env["product.packaging"].create(
            {"product_id": cls.product.id, "uom_id": uom.id, "weight": weight}
        )

    def test_weight_from_packaging(self):
        # 259 = 25 cardbox (250) + 4 pair (8) + 1 unit
        weight = self.product.get_total_weight_from_packaging(259)
        self.assertEqual(weight, 25 * 55 + 4 * 12.5 + 5)

    def test_weight_without_packaging_weight(self):
        # Without any weight on the packagings, fallback on the product weight
        (self.pair_packaging + self.cardbox_packaging).weight = 0
        weight = self.product.get_total_weight_from_packaging(259)
        self.assertEqual(weight, 259 * 5)
