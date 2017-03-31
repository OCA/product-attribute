# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

import odoo.addons.decimal_precision as dp


class CalendarEvent(models.Model):

    _inherit = 'calendar.event'

    template_ids = fields.Many2many(
        string='Products/Services',
        comodel_name='product.template',
        help='Products or services involved in '
             'this event/meeting.'
    )
    min_duration = fields.Float(
        string='Minimum Duration',
        digits=dp.get_precision('Product UoM'),
        compute='_compute_min_duration',
        store=True,
        help='Minimum duration, in hours, the meeting can be.'
    )

    @api.multi
    @api.depends('template_ids')
    def _compute_min_duration(self):
        for record in self:
            min_duration = sum(
                [t.min_service_time for t in record.template_ids]
            )
            record.min_duration = min_duration

    @api.multi
    @api.constrains(
        'template_ids', 'duration', 'start', 'stop', 'min_duration')
    def _check_template_ids(self):
        for record in self:

            event_hours = record.duration
            if not record.duration:
                event_hours = record._get_duration(record.start, record.stop)

            if record.min_duration > event_hours:
                raise ValidationError(
                    _('The services involved require a %s hour '
                      'long meeting.') % record.min_duration,
                )
