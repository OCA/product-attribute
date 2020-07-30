# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import mock
from .common import CommonProductStateHistory
from odoo import fields


class TestProductStateHistory(CommonProductStateHistory):

    def test_history(self):
        with mock.patch.object(fields.Datetime, 'now') as mock_now:
            mock_now.return_value = "2020-07-29 13:00:00"
            self.product_1.state = "end"
        history = self.history_obj.search([
            ('product_template_id', '=', self.product_1.id)],
            limit=1,
        )
        self.assertEquals(
            "2020-07-29 13:00:00",
            history.state_date,
        )
        self.assertEquals(
            "end",
            history.product_state,
        )

        with mock.patch.object(fields.Datetime, 'now') as mock_now:
            mock_now.return_value = "2020-07-29 14:00:00"
            self.product_1.state = "obsolete"

        history = self.history_obj.search([
            ('product_template_id', '=', self.product_1.id)],
            limit=1,
        )
        self.assertEquals(
            "2020-07-29 14:00:00",
            history.state_date,
        )
        self.assertEquals(
            "obsolete",
            history.product_state,
        )

        with mock.patch.object(fields.Datetime, 'now') as mock_now:
            mock_now.return_value = "2020-07-29 15:00:00"
            self.product_2.state = "end"
        history = self.history_obj.search([
            ('product_template_id', '=', self.product_2.id)],
            limit=1,
        )
        self.assertEquals(
            "2020-07-29 15:00:00",
            history.state_date,
        )
        self.assertEquals(
            "end",
            history.product_state,
        )
