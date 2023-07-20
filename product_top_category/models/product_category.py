# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    top_categ_id = fields.Many2one('product.category',
                                   compute="_compute_top_category",
                                   string="Product Top Category",
                                   store=True)

    def _get_top_category(self):
        self.ensure_one()
        if self.parent_id:
            return self.parent_id._get_top_category()
        else:
            return self

    @api.depends('parent_id', 'parent_id.top_categ_id')
    def _compute_top_category(self):
        for categ in self:
            categ.top_categ_id = categ._get_top_category()
