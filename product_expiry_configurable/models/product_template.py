# Copyright 2021 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    compute_dates_from = fields.Selection(
        selection=[
            ("current_date", "Current Date"),
            ("expiration_date", "Expiration Date"),
        ],
        help="If current_date is selected, "
        "the dates will be computed taking as reference "
        "the current date when the lot is created."
        "Whereas if expiration_time is selected,"
        " the dates will be computed taking as reference the lot's expiration_time.",
        compute="_compute_compute_dates_from",
    )
    specific_compute_dates_from = fields.Selection(
        selection=[
            ("current_date", "Current Date"),
            ("expiration_date", "Expiration Date"),
        ],
        help="If current_date is selected, "
        "the dates will be computed taking as reference "
        "the current date when the lot is created."
        "Whereas if expiration_time is selected,"
        " the dates will be computed taking as reference the lot's expiration_date.",
    )
    category_compute_dates_from = fields.Selection(
        string="Category compute dates from",
        help="If current_date is selected, "
        "the dates will be computed taking as reference "
        "the current date when the lot is created."
        "Whereas if expiration_date is selected, "
        "the dates will be computed taking as reference the lot's expiration_date.",
        related="categ_id.compute_dates_from",
    )

    expiration_time = fields.Integer(compute="_compute_date_fields")
    use_time = fields.Integer(compute="_compute_date_fields")
    removal_time = fields.Integer(compute="_compute_date_fields")
    alert_time = fields.Integer(compute="_compute_date_fields")

    specific_expiration_time = fields.Integer(
        string="Specific Product Expiration Time",
        help="Number of days before the goods may "
        "become dangerous and must not be consumed. "
        "It will be computed on the lot/serial number."
        "If not provided, the one defined on the category is used.",
    )
    specific_use_time = fields.Integer(
        string="Specific Product Use Time",
        help="Number of days before the goods starts deteriorating,"
        " without being dangerous yet. "
        "It will be computed using the lot/serial number."
        "If not provided, the one defined on the category is used.",
    )
    specific_removal_time = fields.Integer(
        string="Specific Product Removal Time",
        help="Number of days before the goods should be removed from the stock. "
        "It will be computed on the lot/serial number."
        "If not provided, the one defined on the category is used.",
    )
    specific_alert_time = fields.Integer(
        string="Specific Product Alert Time",
        help="Number of days before an alert should be raised on the lot/serial number."
        "If not provided, the one defined on the category is used.",
    )

    category_expiration_time = fields.Integer(
        string="Category Product Expiration Time",
        help="Number of days before the goods may become "
        "dangerous and must not be consumed. "
        "It will be computed on the lot/serial number.",
        related="categ_id.expiration_time",
    )
    category_use_time = fields.Integer(
        string="Category Product Use Time",
        help="Number of days before the goods starts deteriorating,"
        " without being dangerous yet."
        " It will be computed using the lot/serial number.",
        related="categ_id.use_time",
    )
    category_removal_time = fields.Integer(
        string="Category Product Removal Time",
        help="Number of days before the goods should be removed from the stock. "
        "It will be computed on the lot/serial number.",
        related="categ_id.removal_time",
    )
    category_alert_time = fields.Integer(
        string="Category Product Alert Time",
        help="Number of days before an alert should be raised "
        "on the lot/serial number.",
        related="categ_id.alert_time",
    )

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

    def _get_specific_and_category_date_fields(self):
        specific_dates = ["specific_%s" % date for date in self._get_date_fields()]
        category_dates = ["category_%s" % date for date in self._get_date_fields()]
        return specific_dates + category_dates

    @api.depends(lambda r: r._get_specific_and_category_date_fields())
    def _compute_date_fields(self):
        for rec in self:
            for date in rec._get_date_fields():
                specific_value = getattr(rec, "specific_%s" % date)
                category_value = getattr(rec, "category_%s" % date)
                setattr(rec, date, specific_value or category_value)
