# Copyright 2026 glueckkanja AG
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Declared on the variant as well so that modules giving variants their
    # own ``product_state_id`` (e.g. product_status) are honoured. Without
    # such a module ``product_state_id`` is delegated to the template, so the
    # value is the same as the template one.
    product_state_can_be_invoiced = fields.Boolean(
        related="product_state_id.can_be_invoiced",
        string="State Allows Invoicing",
    )
