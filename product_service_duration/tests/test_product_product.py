# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from mock import patch

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


DATETIME = 'odoo.addons.product_service_duration.models.calendar_event.'\
           'fields.Datetime.now'


class TestProductProduct(TransactionCase):

    def setUp(self):
        super(TestProductProduct, self).setUp()
        self.prod_1 = self.env.ref(
            'product_service_duration.product_product_2'
        )

    @patch(DATETIME)
    def test_check_min_service_time(self, mock_datetime):
        """ Test raise ValidationError if < 0 """
        mock_datetime.return_value = time.strftime('%Y-%m-05 00:00:00')
        with self.assertRaises(ValidationError):
            self.prod_1.min_service_time = -1

    @patch(DATETIME)
    def test_check_event_ids_min_service_time(self, mock_datetime):
        """ Test ValidationError if min_service_time causes conflicts """
        mock_datetime.return_value = time.strftime('%Y-%m-05 00:00:00')
        with self.assertRaises(ValidationError):
            self.prod_1.min_service_time = 100
