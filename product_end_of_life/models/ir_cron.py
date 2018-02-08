# Copyright (C) 2018 - TODAY, Open Source Integrators
# Integrators License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IrCron(models.Model):
    _inherit = 'ir.cron'

    approaching_number = fields.Integer(
        default=1,
        help="Close to X unit(s) to Eol.")
    approaching_type = fields.Selection([
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months')],
        string='Approaching Interval Unit',
        default='months')
