# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AbcClassificationProductLevel(models.Model):

    _inherit = "abc.classification.product.level"

    sale_stock_level_history_ids = fields.One2many(
        comodel_name="abc.sale_stock.level.history",
        inverse_name="product_level_id",
    )
