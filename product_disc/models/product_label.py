# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models, fields


class ProductLabel(models.Model):

    _name = 'product.label'
    _description = 'Record label'
    _order = 'name'

    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner')  # TODO Use inherits ?
    country_ids = fields.Many2many('res.country')  # TODO compute from partner?
