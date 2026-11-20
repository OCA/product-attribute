# Copyright 2026 glueckkanja AG
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_state_can_be_invoiced = fields.Boolean(
        related="product_state_id.can_be_invoiced",
        string="State Allows Invoicing",
        store=True,
    )
