# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv.expression import NEGATIVE_TERM_OPERATORS


class StockProductionLot(models.Model):

    _inherit = "stock.lot"

    product_expiry_alert = fields.Boolean(search="_search_product_expiry_alert")

    expiry_date = fields.Datetime(
        compute="_compute_expiry_date", store=True, index=True
    )

    @api.model
    def _selection_expiry_date_field(self):
        return [
            ("use_date", "Best before Date"),
            ("expiration_date", "Expiration Date"),
            ("alert_date", "Alert date"),
            ("removal_date", "Removal date"),
        ]

    @api.depends(lambda self: self._expiry_date_depends())
    def _compute_expiry_date(self):
        for rec in self:
            rec.expiry_date = rec[rec.product_id.lot_expiry_field_name]

    def _search_product_expiry_alert(self, operator, value):
        search_expired = (
            # product_expiry_alert != False
            (operator in NEGATIVE_TERM_OPERATORS and not value)
            # or product_expiry_alert = True
            or (operator not in NEGATIVE_TERM_OPERATORS and value)
        )
        if search_expired:
            return [("expiry_date", "<", fields.Datetime.now())]
        return [
            "|",
            ("expiry_date", "=", False),
            ("expiry_date", ">=", fields.Datetime.now()),
        ]

    @api.model
    def _expiry_date_depends(self):
        return [f[0] for f in self._selection_expiry_date_field()]

    @api.depends("expiration_date", "expiry_date")
    def _compute_product_expiry_alert(self):
        res = super()._compute_product_expiry_alert()
        for rec in self:
            rec.product_expiry_alert = (
                rec.expiry_date < fields.Datetime.now()
                if rec.expiry_date
                else rec.product_expiry_alert
            )
        return res
