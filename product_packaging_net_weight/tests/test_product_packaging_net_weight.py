# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
from odoo.addons.product.tests.common import ProductCommon


class TestProductPackagingNetWeight(ProductCommon):
    """Tests for the net weight on product.packaging."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))

    def test_net_weight_seeded_then_preserved(self):
        """Packaging net weight is seeded from the product but stays editable.

        Scenario:
            1. Add a dozen packaging to a product with a net weight of 2.
            2. Manually override the packaging net weight to 50.
            3. Make an unrelated edit on the packaging.
        Expected:
            - The packaging is seeded to 24 (per-unit net weight x 12).
            - The manual override survives the unrelated edit.
        """
        product = self._create_product(net_weight=2.0)
        product.packaging_ids = [Command.create({"uom_id": self.uom_dozen.id})]
        packaging = product.packaging_ids
        self.assertEqual(packaging.net_weight, 24.0)  # 2.0 * 12

        packaging.net_weight = 50.0
        packaging.sequence = 5
        self.assertEqual(packaging.net_weight, 50.0)

    def test_net_weight_kept_on_product_change(self):
        """Changing the product's net weight leaves its packagings untouched.

        Scenario:
            1. Add a dozen packaging to a product with a net weight of 2.
            2. Change the product's net weight.
        Expected:
            - The packaging keeps the value it was seeded with, rather than
              having a possibly user-defined value overwritten.
        """
        product = self._create_product(net_weight=2.0)
        product.packaging_ids = [Command.create({"uom_id": self.uom_dozen.id})]
        packaging = product.packaging_ids
        self.assertEqual(packaging.net_weight, 24.0)  # 2.0 * 12

        product.net_weight = 5.0
        self.assertEqual(packaging.net_weight, 24.0)

    def test_net_weight_reseed_on_uom_change(self):
        """Changing a packaging's UoM recomputes its net weight.

        Scenario:
            1. Add a dozen packaging to a product with a net weight of 2.
            2. Change that packaging's UoM to a pack of 6.
        Expected:
            - The net weight is re-seeded from 24 to 12.
        """
        product = self._create_product(net_weight=2.0)
        product.packaging_ids = [Command.create({"uom_id": self.uom_dozen.id})]
        packaging = product.packaging_ids
        self.assertEqual(packaging.net_weight, 24.0)  # 2.0 * 12

        packaging.uom_id = self.uom_pack_6  # qty 6
        self.assertEqual(packaging.qty, 6)
        self.assertEqual(packaging.net_weight, 12.0)  # 2.0 * 6
