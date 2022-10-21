# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    top_categ_id = fields.Many2one('product.category',
                                   related='categ_id.top_categ_id',
                                   store=True)
