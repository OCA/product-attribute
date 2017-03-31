# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

import time


class TesteventEvent(TransactionCase):

    def setUp(self):
        super(TesteventEvent, self).setUp()
        self.templ_1 = self.env.ref(
            'product_service_duration.product_template_1'
        )
        self.templ_2 = self.env.ref(
            'product_service_duration.product_template_2'
        )
        self.event_1 = self.env.ref(
            'product_service_duration.calendar_event_1'
        )

    def test_event_match_duration(self):
        """ Test no error if sum tmpl durations match event duration """
        try:
            self.event_1.duration = 5.00
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise error if '
                'sum of template durations match '
                'event duration.'
            )

    def test_event_less_duration(self):
        """ Test no error if sum tmpl durations less than event duration """
        try:
            self.event_1.duration = 7.00
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise error if '
                'sum of template durations greater than '
                'event duration.'
            )

    def test_event_more_duration(self):
        """ Test error if sum tmpl durations greater than event duration """
        with self.assertRaises(ValidationError):
            self.event_1.duration = 4.00

    def test_event_match_duration_no_event_duration(self):
        """ Test no error if sum tmpl durations match event no duration """
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

    def test_event_less_duration_no_event_duration(self):
        """ Test no error if sum tmpl durations less than event no duration """
        self.event_1.duration = None
        try:
            self.event_1.stop = time.strftime('%Y-%m-10 19:00:00')
            self.assertTrue(True)
        except ValidationError:
            self.fail(
                'Should not raise error if '
                'sum of template durations greater than '
                'event duration.'
            )

    def test_event_more_duration_no_event_duration(self):
        """ Test error if sum tmpl durations greater than event no duration """
        self.event_1.duration = None
        with self.assertRaises(ValidationError):
            self.event_1.stop = time.strftime('%Y-%m-10 16:00:00')
