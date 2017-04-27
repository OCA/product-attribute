# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from mock import patch

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


DATETIME = 'odoo.addons.product_service_duration.models.calendar_event.'\
           'fields.Datetime.now'


class TestCalendarEvent(TransactionCase):

    def setUp(self):
        super(TestCalendarEvent, self).setUp()
        self.prod_1 = self.env.ref(
            'product_service_duration.product_product_1'
        )
        self.prod_2 = self.env.ref(
            'product_service_duration.product_product_2'
        )
        self.event_1 = self.env.ref(
            'product_service_duration.calendar_event_1'
        )

    @patch(DATETIME)
    def test_stop_date_in_future_min_service_time(self, mock_datetime):
        """ Test no validation error raised if event is allday """
        mock_datetime.return_value = time.strftime('%Y-%m-20 00:00:00')
        self.event_1.stop = time.strftime('%Y-%m-10 17:00:00')
        try:
            self.prod_1.min_service_time = 20.0
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise a validation error '
                'if event stop date is in future.'
            )

    @patch(DATETIME)
    def test_event_all_day(self, mock_datetime):
        """ Test no validation error if event is all day """
        mock_datetime.return_value = time.strftime('%Y-%m-05 00:00:00')
        self.event_1.allday = True
        self.prod_1.min_service_time = 3.00
        try:
            self.event_1.duration = 4.00
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise ValidationError '
                'if event is allday'
            )

    @patch(DATETIME)
    def test_stop_date_in_future_duration(self, mock_datetime):
        """ Test no validation error raised if stop date in future """
        mock_datetime.return_value = time.strftime('%Y-%m-20 00:00:00')
        self.event_1.stop = time.strftime('%Y-%m-10 17:00:00')
        self.prod_1.min_service_time = 1.0
        try:
            self.event_1.duration = 0.0
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise a validation error '
                'if event stop date is in future.'
            )

    @patch(DATETIME)
    def test_products_min_service_time_zero(self, mock_datetime):
        """ Test min_duration 0 if sum prod service times 0 """
        mock_datetime.return_value = time.strftime('%Y-%m-05 00:00:00')
        self.prod_1.min_service_time = 0.0
        self.prod_2.min_service_time = 0.0
        self.assertEquals(
            self.event_1.min_duration,
            0.0,
        )

    @patch(DATETIME)
    def test_event_match_duration(self, mock_datetime):
        """ Test no error if sum prod service times match event duration """
        mock_datetime.return_value = time.strftime('%Y-%m-05 00:00:00')
        self.prod_1.min_service_time = 3.00
        try:
            self.event_1.duration = 5.00
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise error if '
                'sum of template durations match '
                'event duration.'
            )

    @patch(DATETIME)
    def test_event_less_duration(self, mock_datetime):
        """ Test no error if sum prod service time less than event duration """
        mock_datetime.return_value = time.strftime('%Y-%m-05 00:00:00')
        self.prod_1.min_service_time = 3.00
        try:
            self.event_1.duration = 7.00
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise error if '
                'sum of template durations greater than '
                'event duration.'
            )

    @patch(DATETIME)
    def test_event_more_duration(self, mock_datetime):
        """ Test error if sum prod service time greater than event duration """
        mock_datetime.return_value = time.strftime('%Y-%m-05 00:00:00')
        self.prod_1.min_service_time = 3.00
        with self.assertRaises(ValidationError):
            self.event_1.duration = 1.00

    @patch(DATETIME)
    def test_event_match_duration_no_event_duration(self, mock_datetime):
        """ Test no error if sum tmpl durations match event no duration """
        mock_datetime.return_value = time.strftime('%Y-%m-05 00:00:00')
        self.prod_1.min_service_time = 3.00
        self.event_1.duration = None
        try:
            self.event_1.stop = time.strftime('%Y-%m-10 17:00:00')
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise error if '
                'sum of template durations match '
                'event duration.'
            )

    @patch(DATETIME)
    def test_event_less_duration_no_event_duration(self, mock_datetime):
        """ Test no error if sum prod serv time less than event no duration """
        mock_datetime.return_value = time.strftime('%Y-%m-05 00:00:00')
        self.event_1.duration = None
        self.prod_1.min_service_time = 3.00
        try:
            self.event_1.stop = time.strftime('%Y-%m-10 19:00:00')
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise error if '
                'sum of template durations greater than '
                'event duration.'
            )

    @patch(DATETIME)
    def test_event_more_duration_no_event_duration(self, mock_datetime):
        """ Test error if sum prod serv time greater than event no duration """
        mock_datetime.return_value = time.strftime('%Y-%m-05 00:00:00')
        self.prod_1.min_service_time = 3.00
        self.event_1.duration = None
        with self.assertRaises(ValidationError):
            self.event_1.stop = time.strftime('%Y-%m-10 16:00:00')
