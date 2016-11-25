# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from datetime import datetime

_KOSHER_STATE = [
    ('certified', 'Certified'),
    ('not_certified', 'Not Certified')
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    @api.depends(
        "kosher_ids",
        "kosher_ids.name",
        "kosher_ids.date_start",
        "kosher_ids.date_end",
    )
    def _compute_kosher_state(self):
        date_now = datetime.now().strftime("%Y-%m-%d")
        for product in self:
            product.kosher_id = False
            if product.kosher_ids:
                kosher = product.kosher_ids[0]
                if not kosher.date_end:
                    product.kosher_state = "certified"
                    product.kosher_id = kosher
                else:
                    if kosher.date_end > date_now:
                        product.kosher_state = "certified"
                        product.kosher_id = kosher
                    else:
                        product.kosher_state = "not_certified"
            else:
                product.kosher_state = "not_certified"

    kosher_ids = fields.One2many(
        string="Product Kosher",
        comodel_name="product.kosher",
        inverse_name="product_tmpl_id"
    )
    kosher_id = fields.Many2one(
        string="Active Kosher Certificate",
        comodel_name="product.kosher",
        compute="_compute_kosher_state",
    )
    kosher_state = fields.Selection(
        string="Kosher Status",
        compute="_compute_kosher_state",
        selection=_KOSHER_STATE,
        store=True
    )
