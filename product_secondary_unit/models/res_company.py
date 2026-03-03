# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    # Added for supporting the existing report presentation. We can drop this together
    # with the second qty column in reports if the community agrees with it.
    hide_secondary_uom_column_sale = fields.Boolean(
        string="Hide Secondary UoM Column (Sales)",
        default=False,
    )
    hide_secondary_uom_column_purchase = fields.Boolean(
        string="Hide Secondary UoM Column (Purchase)",
        default=False,
    )

    def hide_secondary_uom_column(self, record):
        """Return whether to hide the 'Second Qty' column for this document type."""
        if record._name == "sale.order" or (
            record._name == "account.move"
            and record.is_sale_document(include_receipts=True)
        ):
            return self.hide_secondary_uom_column_sale
        if record._name == "purchase.order" or (
            record._name == "account.move"
            and record.is_purchase_document(include_receipts=True)
        ):
            return self.hide_secondary_uom_column_purchase
        return True
