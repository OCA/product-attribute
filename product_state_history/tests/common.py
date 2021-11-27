# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import SavepointCase


class CommonProductStateHistory(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(CommonProductStateHistory, cls).setUpClass()
        cls.product_1 = cls.env.ref("product.product_delivery_01")
        cls.product_2 = cls.env.ref("product.product_delivery_02")
        cls.history_obj = cls.env["product.state.history"]
        cls.history_wizard_obj = cls.env["product.state.history.wizard"]
        cls.end = cls.env.ref("product_state.product_state_end")
        cls.obsolete = cls.env.ref("product_state.product_state_obsolete")
        if not cls.env.company.external_report_layout_id:
            cls.env.company.external_report_layout_id = cls.env.ref(
                "web.external_layout_background"
            )
