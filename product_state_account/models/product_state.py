# Copyright 2026 glueckkanja AG
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductState(models.Model):
    _inherit = "product.state"

    can_be_invoiced = fields.Boolean(
        default=True,
        help="Products in this state can be selected on customer invoices.",
    )
