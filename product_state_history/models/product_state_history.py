# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductStateHistory(models.Model):

    _name = 'product.state.history'
    _description = 'Product State History'
    _order = 'id desc'
    _rec_name = 'product_template_id'

    product_template_id = fields.Many2one(
        comodel_name="product.template",
        string="Product",
        required=True,
        ondelete='cascade',
        index=True,
    )
    product_state = fields.Selection(
        selection=[
            ('draft', 'In Development'),
            ('sellable', 'Normal'),
            ('end', 'End of Lifecycle'),
            ('obsolete', 'Obsolete')
        ],
        string='Status',
        index=True,
        required=True,
    )
    state_date = fields.Datetime(
        default=lambda s: fields.Datetime.now(),
        string="Date",
        required=True,
        index=True,
    )
