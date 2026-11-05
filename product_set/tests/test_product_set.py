# Copyright 2015 Anybox S.A.S
# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import Command

from .common import ProductSetCommon


class TestProductSet(ProductSetCommon):
    """Test Product set"""

    def test_name(self):
        product_set = self.product_set_1
        # no ref
        product_set.name = "Foo"
        product_set.ref = ""
        self.assertEqual(
            product_set.read(["display_name"]),
            [{"id": product_set.id, "display_name": "Foo"}],
        )
        # with ref
        product_set.ref = "123"
        self.assertEqual(
            product_set.read(["display_name"]),
            [{"id": product_set.id, "display_name": "[123] Foo"}],
        )
        # with partner
        product_set.partner_id = self.partner_1
        self.assertEqual(
            product_set.read(["display_name"]),
            [
                {
                    "id": product_set.id,
                    "display_name": f"[123] Foo @ {self.partner_1.name}",
                }
            ],
        )

    def test_active(self):
        """Test the archive/unarchive of the set and its lines."""
        product_2 = self.env["product.product"].create({"name": "Test Product 2"})
        prod_set = self.env["product.set"].create(
            {
                "name": "Test",
                "set_line_ids": [
                    Command.create({"product_id": self.product.id}),
                    Command.create({"product_id": product_2.id}),
                ],
            }
        )
        self.assertTrue(prod_set.active)
        all_lines = prod_set.set_line_ids.with_context(active_test=False)
        self.assertTrue(all(all_lines.mapped("active")))
        all_lines[0].active = False
        self.assertTrue(all_lines[1].active)
        prod_set.active = False
        self.assertTrue(all(not x for x in all_lines.mapped("active")))
