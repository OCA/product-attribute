# Copyright 2021 Camptocamp SA
# @author: Julien Coux <julien.coux@camptocamp.com>
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# @author: Damien Crier <damien.crier@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductAllowedListLine(models.Model):
    _inherit = "product.allowed.list.line"

    date_start = fields.Datetime(required=True)
    date_end = fields.Datetime()
    monday = fields.Boolean(default=True)
    tuesday = fields.Boolean(default=True)
    wednesday = fields.Boolean(default=True)
    thursday = fields.Boolean(default=True)
    friday = fields.Boolean(default=True)
    saturday = fields.Boolean(default=True)
    sunday = fields.Boolean(default=True)

    @api.constrains("date_start", "date_end")
    def _check_date_end(self):
        for line in self:
            if line.date_end and line.date_end < line.date_start:
                raise ValidationError(
                    _("The end date cannot be earlier than the start date.")
                )

    def is_sale_ok(self, date):
        self.ensure_one()

        weekday = date.strftime("%A").lower()
        # check if we are on the correct day of the week
        if not self[weekday]:
            return False

        date_end = self.date_end or date
        return self.date_start <= date <= date_end
