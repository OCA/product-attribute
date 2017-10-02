# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    stock_state = fields.Selection([
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out Of Stock'),
        ('resupplying', 'Resupplying'),
        ('in_limited_stock', 'In Limited Stock'),
        ],
        compute='_compute_stock_state')

    def _get_stock_state(self):
        self.ensure_one()
        if not self.sale_ok:
            return 'out_of_stock'
        elif self.qty_available <= 0:
            return 'resupplying'
        elif self.qty_available <= self._level_for_limited_stock():
            return 'in_limited_stock'
        else:
            return 'in_stock'

    def _compute_stock_state(self):
        for record in self:
            record.stock_state = record._get_stock_state()

    def _level_for_limited_stock(self):
        return 10
