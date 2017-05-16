# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

import odoo.addons.decimal_precision as dp


class ProductProduct(models.Model):

    _inherit = 'product.product'

    resource_id = fields.Many2one(
        string='Resource',
        comodel_name='resource.resource',
        help='Optionally set a resource on performing this service',
    )
    min_service_time = fields.Float(
        string='Minimum Time',
        digits=dp.get_precision('Product UoM'),
        help='Minimum time it takes to complete this service in hours.',
    )
    event_ids = fields.Many2many(
        string='Events/Meetings',
        comodel_name='calendar.event',
        help='Events or meetings this service '
             'is involved in.',
    )

    @api.multi
    @api.constrains('min_service_time')
    def _check_min_service_time(self):
        for record in self:
            if record.min_service_time < 0:
                raise ValidationError(_(
                    'Minimum Time cannot be less than 0.'
                ))

    @api.multi
    @api.constrains('min_service_time', 'event_ids')
    def _check_event_ids_min_service_time(self):
        for record in self:
            for event in record.event_ids:
                try:
                    event._compute_min_duration()
                except ValidationError:
                    raise ValidationError(
                        _('The minimum service time for this product is '
                          'causing issues with at least one meeting: %s.') %
                        event.display_name,
                    )
