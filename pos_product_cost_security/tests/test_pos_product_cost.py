# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestPosProductCostSecurity(HttpCase):
    def setUp(self):
        super().setUp()
        # Ensure that the pricelist is correctly localized
        self.pricelist = self.env["product.pricelist"].create(
            {
                "name": "Test pricelist",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "compute_price": "formula",
                            "base": "list_price",
                        },
                    )
                ],
            }
        )
        self.pos_config = self.env.ref("point_of_sale.pos_config_main")
        self.pos_config.write(
            {
                "available_pricelist_ids": [(6, 0, self.pricelist.ids)],
                "pricelist_id": self.pricelist.id,
            }
        )

    def test_pos_session_open(self):
        self.pos_config.with_user(self.env.ref("base.user_demo")).open_session_cb()
        self.start_tour(
            "/pos/ui?config_id=%d" % self.pos_config.id,
            "pos_product_cost",
            login="demo",
        )
