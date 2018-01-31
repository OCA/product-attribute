# Copyright (C) 2017 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    firmware_version = fields.Char(
        string='Firmware Version'
    )
