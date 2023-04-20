# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    use_expiration_date = fields.Boolean(
        compute="_compute_use_expiration_date", readonly=False, store=True
    )
    expiration_time = fields.Integer(
        compute="_compute_date_fields",
        store=True,
        readonly=False,
    )
    use_time = fields.Integer(
        compute="_compute_date_fields",
        store=True,
        readonly=False,
    )
    removal_time = fields.Integer(
        compute="_compute_date_fields",
        store=True,
        readonly=False,
    )
    alert_time = fields.Integer(
        compute="_compute_date_fields",
        store=True,
        readonly=False,
    )

    @api.depends("categ_id.use_expiration_date")
    def _compute_use_expiration_date(self):
        for template in self:
            template.use_expiration_date = template.categ_id.use_expiration_date

    def _get_date_fields(self):
        return ["expiration_time", "use_time", "removal_time", "alert_time"]

    @api.depends("specific_compute_dates_from", "category_compute_dates_from")
    def _compute_compute_dates_from(self):
        for rec in self:
            rec.compute_dates_from = (
                rec.specific_compute_dates_from
                or rec.category_compute_dates_from
                or "current_date"
            )

    def _get_category_date_fields_depends(self):
        return ["categ_id.%s" % date_field for date_field in self._get_date_fields()]

    @api.depends(lambda self: self._get_category_date_fields_depends())
    def _compute_date_fields(self):
        for rec in self:
            for date in rec._get_date_fields():
                # Set the field value from its category one
                value = getattr(rec.categ_id, "%s" % date)
                setattr(rec, date, value)
