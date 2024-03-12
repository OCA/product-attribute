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
        self.assertEqual(product_set.name_get(), [(product_set.id, "Foo")])
        # with ref
        product_set.ref = "123"
        self.assertEqual(product_set.name_get(), [(product_set.id, "[123] Foo")])
        # with partner
        partner = self.env.ref("base.res_partner_1")
        product_set.partner_id = partner
        self.assertEqual(
            product_set.name_get(), [(product_set.id, "[123] Foo @ %s" % partner.name)]
        )
