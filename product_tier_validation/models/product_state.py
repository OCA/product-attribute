# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductState(models.Model):
    _inherit = "product.state"

    state = fields.Selection(
        [("draft", "To Approve"), ("confirmed", "Approved"), ("cancel", "Archived")],
        string="Related State",
        default="confirmed",
        help="""Tier validation uses specific states (To and From) to trigger
              validation needs. Since the Code field is a unique and user defined
              field, this state field provides the states used for valdiation.""",
    )
