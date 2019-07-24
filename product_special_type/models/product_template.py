# -*- coding: utf-8 -*-
# Copyright 2012-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    special_type = fields.Selection(
        selection=lambda self: self._get_special_type_selection(),
        help='Special products will not be displayed on document lines '
             'invoices but will be summed in the totals.'
    )

    @api.model
    def _get_special_type_selection(self):
        return [
            ('discount', 'Global Discount'),
            ('advance', 'Advance'),
            ('delivery', 'Delivery Costs'),
            ('fee', 'Fee'),
        ]
