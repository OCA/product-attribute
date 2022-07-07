# Copyright 2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from ast import literal_eval
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_eol_approaching_number = fields.Integer(
        default=1,
        help="Close to X unit(s) to Eol.")
    product_eol_approaching_type = fields.Selection([
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months')],
        string='Approaching Interval Unit',
        default='months')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param

        res.update(
            product_eol_approaching_number=literal_eval(get_param(
                'product_end_of_life.approaching_number', default='1'
            )),
            product_eol_approaching_type=literal_eval(get_param(
                'product_end_of_life.approaching_type', default="'months'"
            ))
        )

        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param

        set_param('product_end_of_life.approaching_number',
                  repr(self.product_eol_approaching_number))
        set_param('product_end_of_life.approaching_type',
                  repr(self.product_eol_approaching_type))
