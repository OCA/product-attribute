# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    bundle_id = fields.Many2one(
        comodel_name="product.product", string="Product bundle",
        readonly=True)
