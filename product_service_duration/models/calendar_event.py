# Copyright 2017 LasLabs Inc.
# © initOS GmbH 2019
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

import odoo.addons.decimal_precision as dp


class CalendarEvent(models.Model):

    _inherit = 'calendar.event'

    product_ids = fields.Many2many(
        string='Services',
        comodel_name='product.product',
        help='Services involved in '
             'this event/meeting.',
        domain="[('type', '=', 'service')]",
    )
    min_duration = fields.Float(
        string='Minimum Duration',
        digits=dp.get_precision('Product UoM'),
        compute='_compute_min_duration',
        store=True,
        help='Minimum duration, in hours, the meeting can be.'
    )

    @api.multi
    @api.depends(
        'product_ids', 'product_ids.min_service_time', 'stop', 'allday')
    def _compute_min_duration(self):
        today_time = fields.Datetime.now()
        for record in self:
            if record.stop:
                if record.stop < today_time:
                    continue

                if record.allday:
                    continue

            min_duration = sum(
                [t.min_service_time for t in record.product_ids]
            )

            if min_duration < 0:
                min_duration = 0

            record.min_duration = min_duration

    @api.multi
    @api.constrains(
        'product_ids', 'duration', 'start', 'stop', 'min_duration')
    def _check_product_ids(self):
        today_time = fields.Datetime.now()
        for record in self:

            if record.stop < today_time:
                continue

            if record.allday:
                continue

            event_hours = record.duration

            if not event_hours:
                event_hours = record._get_duration(record.start, record.stop)

            if record.min_duration > event_hours:
                raise ValidationError(
                    _('The services involved require a %s hour '
                      'long meeting.') % record.min_duration,
                )
