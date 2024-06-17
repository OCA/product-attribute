# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import tagged, users

from odoo.addons.point_of_sale.tests.common import TestPointOfSaleCommon, TestPoSCommon


@tagged("post_install", "-at_install")
class TestPosProductCostSecurity(TestPointOfSaleCommon, TestPoSCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config = cls.basic_config

    @users("demo")
    def test_pos_session_open(self):
        self.session = self.open_new_session()
