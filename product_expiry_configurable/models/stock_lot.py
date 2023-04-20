# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime

from odoo import SUPERUSER_ID, _, api, fields, models


class StockLot(models.Model):

    _inherit = "stock.lot"

    use_date_reminded = fields.Boolean(default=False)

    removal_date_reminded = fields.Boolean(default=False)

    expiration_date_reminded = fields.Boolean(default=False)

    def _get_dates_from_expiration_date(
        self, product, mapped_fields, expiration_date=False
    ):
        res = dict.fromkeys(mapped_fields, False)
        expiration_date = self.expiration_date or expiration_date
        for field in mapped_fields:
            duration = getattr(product, mapped_fields[field])
            if duration and expiration_date:
                date = expiration_date - datetime.timedelta(days=duration)
                res[field] = fields.Datetime.to_string(date)
        return res

    def _search_quants_domain(self, expiry_lots):
        return [
            ("lot_id", "in", expiry_lots.ids),
            ("quantity", ">", 0),
            ("location_id.usage", "=", "internal"),
            ("location_id.scrap_location", "=", False),
        ]

    def _get_expired_lots_domain_for_remind(self, date_field, date_reminded_field):
        return [
            (date_field, "<=", fields.Date.today()),
            (date_reminded_field, "=", False),
        ]

    @api.model
    def _expiry_date_exceeded(self, date_field=False):
        """Log an activity on internally stored lots whose "date" field has been reached.
        No further activity will be generated on lots whose "date"
        has already been reached (even if the "date" is changed).
        """
        date_reminded_field = "%s_reminded" % date_field
        expiry_lots = self.env["stock.lot"].search(
            self._get_expired_lots_domain_for_remind(date_field, date_reminded_field)
        )

        lot_stock_quants = self.env["stock.quant"].search(
            self._search_quants_domain(expiry_lots)
        )

        expiry_lots = lot_stock_quants.mapped("lot_id")

        date_name = self._fields[date_field].string

        for lot in expiry_lots:
            lot.activity_schedule(
                "product_expiry_configurable.mail_activity_type_expiry_date_reached",
                user_id=lot.product_id.responsible_id.id or SUPERUSER_ID,
                note=_(
                    "The {date_name} has been reached for this lot/serial number"
                ).format(date_name=date_name),
            )

        expiry_lots.write({date_reminded_field: True})
