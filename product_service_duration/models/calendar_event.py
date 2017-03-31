# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CalendarEvent(models.Model):

    _inherit = 'calendar.event'

    template_ids = fields.Many2many(
        string='Products/Services',
        comodel_name='product.template',
        help='Products or services involved in '
             'this event/meeting.'
    )

    @api.multi
    @api.constrains('template_ids', 'duration', 'start', 'stop')
    def _check_template_ids(self):
        for record in self:

            event_hours = record.duration

            if not event_hours:
                start = fields.Datetime.from_string(
                    record.start
                )
                stop = fields.Datetime.from_string(
                    record.stop
                )

                diff_secs = (stop - start).total_seconds()
                event_hours = diff_secs / 3600

            min_event_duration = sum(
                [t.minimum_service_time for t in record.template_ids]
            )
            if min_event_duration > event_hours:
                raise ValidationError(_(
                    'The services involved requires a %s hour '
                    'long meeting.' % min_event_duration,
                ))
