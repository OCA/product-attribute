# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime

from odoo import SUPERUSER_ID, _, api, fields, models


class StockProductionLot(models.Model):

    _inherit = "stock.production.lot"

    use_date_reminded = fields.Boolean(default=False)

    removal_date_reminded = fields.Boolean(default=False)

    life_date_reminded = fields.Boolean(default=False)

    def _get_dates_from_life_date(self, product, mapped_fields, life_date=False):
        res = dict.fromkeys(mapped_fields, False)
        life_date = self.life_date or life_date
        for field in mapped_fields:
            duration = getattr(product, mapped_fields[field])
            if duration and life_date:
                date = life_date - datetime.timedelta(days=duration)
                res[field] = fields.Datetime.to_string(date)
        return res

    def _get_dates(self, product_id=None):
        """Returns dates based on number of days configured in current lot's product.
            The date will be computed depending on the field 'compute_dates_from'"""
        mapped_fields = {
            "use_date": "use_time",
            "removal_date": "removal_time",
            "alert_date": "alert_time",
        }
        product = self.env["product.product"].browse(product_id) or self.product_id
        res = dict.fromkeys(mapped_fields, False)
        life_date = self.life_date or self.env.context.get("life_date")
        if product and product.tracking != "none":
            if product.compute_dates_from == "life_date" and life_date:
                res = self._get_dates_from_life_date(product, mapped_fields, life_date)
            elif product.compute_dates_from == "current_date":
                res = super()._get_dates(product_id=product_id)
        return res

    @api.onchange("life_date")
    def _onchange_life_date(self):
        if self.product_id.compute_dates_from == "life_date":
            dates_dict = self._get_dates()
            for field, value in dates_dict.items():
                setattr(self, field, value)

    @api.model
    def create(self, vals):
        dates = self.with_context(life_date=vals.get("life_date"))._get_dates(
            vals.get("product_id") or self.env.context.get("default_product_id")
        )
        for d in dates:
            if not vals.get(d):
                vals[d] = dates[d]
        return super(StockProductionLot, self).create(vals)

    def _search_quants_domain(self, expiry_lots):
        return [
            ("lot_id", "in", expiry_lots.ids),
            ("quantity", ">", 0),
            ("location_id.usage", "=", "internal"),
            ("location_id.scrap_location", "=", False),
        ]

    @api.model
    def _expiry_date_exceeded(self, date_field=False):
        """Log an activity on internally stored lots whose "date" field has been reached.
        No further activity will be generated on lots whose "date"
        has already been reached (even if the "date" is changed).
        """

        date_reminded_field = "%s_reminded" % date_field

        expiry_lots = self.env["stock.production.lot"].search(
            [(date_field, "<=", fields.Date.today()), (date_reminded_field, "=", False)]
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
                    "The %s has been reached for this lot/serial number" % date_name
                ),
            )

        expiry_lots.write({date_reminded_field: True})
