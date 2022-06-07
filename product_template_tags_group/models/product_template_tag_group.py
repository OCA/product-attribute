#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplateTagGroup (models.Model):
    _name = 'product.template.tag.group'
    _description = 'Product Tag Group'
    _rec_name = 'name'

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
    )
    tag_ids = fields.One2many(
        comodel_name='product.template.tag',
        inverse_name='tag_group_id',
        string="Tags",
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string="Company",
        default=lambda self: self.env['res.company']._company_default_get(),
    )
