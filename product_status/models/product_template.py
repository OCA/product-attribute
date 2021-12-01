# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models

other_date_fields = {
    "end_of_life_date": {"new_until": False, "discontinued_until": False},
    "discontinued_until": {"new_until": False},
}


class ProductTemplate(models.Model):

    _inherit = "product.template"

    end_of_life_date = fields.Date(
        string="End-of-life",
        help="When the product is end-of-life, and you want to warn your "
        "client/avoid order in the future.",
    )
    discontinued_until = fields.Date(
        string="Discontinued until",
        help="When the product is discontinued for a certain time, to warn "
        "your client/avoid order during this downtime.",
    )
    new_until = fields.Date(
        string="New until",
        help="New product, and you want to warn your client for a certain time",
    )

    @api.onchange("end_of_life_date")
    def _onchange_end_of_life_date(self):
        for rec in self:
            self._update_dates_of_states(rec, "end_of_life_date")

    @api.onchange("discontinued_until")
    def _onchange_discontinued_until(self):
        for rec in self:
            self._update_dates_of_states(rec, "discontinued_until")

    @api.model
    def _update_dates_of_states(self, record, date_field):
        if not getattr(record, date_field):
            return
        record.update(other_date_fields[date_field])

    @api.depends(
        "product_state_id", "new_until", "end_of_life_date", "discontinued_until"
    )
    def _compute_product_state(self):
        for record in self:
            self._check_dates_of_states(record)

    # This method can be called by variant so the record is either
    # product.template or product.product
    @api.model
    def _check_dates_of_states(self, record):
        today = fields.Date.today()
        if record.end_of_life_date:
            if record.end_of_life_date < today:
                record.state = "endoflife"
            else:
                record.state = "phaseout"
        elif record.discontinued_until and record.discontinued_until >= today:
            record.state = "discontinued"
        elif record.new_until and record.new_until >= today:
            record.state = "new"
        else:
            if record._name == "product.template":
                product_state = record.product_state_id
            else:
                product_state = record.product_tmpl_id.product_state_id
            record.state = product_state.code
        # This is not triggered when assigning value in code.
        record._inverse_product_state()
