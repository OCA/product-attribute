# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    service_user_id = fields.Many2one(
        string='Service User',
        comodel_name='res.users',
        help='Optionally set a user on performing this service',
    )
    minimum_service_time = fields.Float(
        string='Minimum Service Hours',
        digits_compute=dp.get_precision('Product UoM'),
        help='Minimum time it takes to complete this service in hours.',
    )
    event_ids = fields.Many2many(
        string='Events/Meetings',
        comodel_name='calendar.event',
        help='Events or meetings this product/service '
             'is involved in.',
    )
