# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.osv.expression import NEGATIVE_TERM_OPERATORS


class StockLot(models.Model):

    _inherit = "stock.lot"

    product_use_date_expiry_alert = fields.Boolean(
        compute="_compute_product_use_date_expiry_alert",
        search="_search_product_use_date_expiry_alert",
        help="This field means the use date is expired.",
    )
    product_removal_date_expiry_alert = fields.Boolean(
        compute="_compute_product_removal_date_expiry_alert",
        search="_search_product_removal_date_expiry_alert",
        help="This field means the removal date is expired.",
    )
    product_alert_date_expiry_alert = fields.Boolean(
        compute="_compute_product_alert_date_expiry_alert",
        search="_search_product_alert_date_expiry_alert",
        help="This field means the alert date is expired.",
    )

    @api.depends("use_date")
    def _compute_product_use_date_expiry_alert(self):
        current_date = fields.Datetime.now()
        for lot in self:
            if lot.use_date:
                lot.product_use_date_expiry_alert = lot.use_date <= current_date
            else:
                lot.product_use_date_expiry_alert = False

    @api.depends("removal_date")
    def _compute_product_removal_date_expiry_alert(self):
        current_date = fields.Datetime.now()
        for lot in self:
            if lot.removal_date:
                lot.product_removal_date_expiry_alert = lot.removal_date <= current_date
            else:
                lot.product_removal_date_expiry_alert = False

    @api.depends("alert_date")
    def _compute_product_alert_date_expiry_alert(self):
        current_date = fields.Datetime.now()
        for lot in self:
            if lot.alert_date:
                lot.product_alert_date_expiry_alert = lot.alert_date <= current_date
            else:
                lot.product_alert_date_expiry_alert = False

    def _search_product_use_date_expiry_alert(self, operator, value):
        current_date = fields.Datetime.now()
        if (operator in NEGATIVE_TERM_OPERATORS and value) or (
            operator not in NEGATIVE_TERM_OPERATORS and not value
        ):
            domain = ["|", ("use_date", "=", False), ("use_date", ">", current_date)]
        else:
            domain = [("use_date", "<=", current_date)]
        return domain

    def _search_product_removal_date_expiry_alert(self, operator, value):
        current_date = fields.Datetime.now()
        if (operator in NEGATIVE_TERM_OPERATORS and value) or (
            operator not in NEGATIVE_TERM_OPERATORS and not value
        ):
            domain = [
                "|",
                ("removal_date", "=", False),
                ("removal_date", ">", current_date),
            ]
        else:
            domain = [("removal_date", "<=", current_date)]
        return domain

    def _search_product_alert_date_expiry_alert(self, operator, value):
        current_date = fields.Datetime.now()
        if (operator in NEGATIVE_TERM_OPERATORS and value) or (
            operator not in NEGATIVE_TERM_OPERATORS and not value
        ):
            domain = [
                "|",
                ("alert_date", "=", False),
                ("alert_date", ">", current_date),
            ]
        else:
            domain = [("alert_date", "<=", current_date)]
        return domain
