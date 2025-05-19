# Copyright 2015 Anybox S.A.S
# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import common


class TestProductSet(common.TransactionCase):
    """Test Product set"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product_set = cls.env.ref("product_set.product_set_i5_computer")

    def test_name(self):
        product_set = self.product_set
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
        partner = self.env.ref("base.res_partner_1")
        product_set.partner_id = partner
        self.assertEqual(
            product_set.read(["display_name"]),
            [{"id": product_set.id, "display_name": f"[123] Foo @ {partner.name}"}],
        )

    def test_active(self):
        """Test the archive/unarchive of the set and its lines."""
        prod_set = self.env["product.set"].create(
            {
                "name": "Test",
                "set_line_ids": [
                    (
                        0,
                        0,
                        {"product_id": self.env.ref("product.product_product_1").id},
                    ),
                    (
                        0,
                        0,
                        {"product_id": self.env.ref("product.product_product_2").id},
                    ),
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
