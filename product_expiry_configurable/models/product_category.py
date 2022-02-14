# Copyright 2022 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductCategory(models.Model):

    _inherit = "product.category"

    compute_dates_from = fields.Selection(
        selection=[("current_date", "Current Date"), ("life_date", "Life Time Date")],
        help="If current_date is selected, the dates will be computed taking "
        "as reference the current date when the lot is created."
        "Whereas if life_date is selected, "
        "the dates will be computed taking as reference the lot's life_date.",
        compute="_compute_compute_dates_from",
    )
    specific_compute_dates_from = fields.Selection(
        selection=[("current_date", "Current Date"), ("life_date", "Life Time Date")],
        help="If not provided, the one defined on the parent is used.",
    )
    parent_compute_dates_from = fields.Selection(
        selection=[("current_date", "Current Date"), ("life_date", "Life Time Date")],
        compute="_compute_parent_compute_dates_from",
    )

    life_time = fields.Integer(
        string="Product Life Time",
        help="Number of days before the goods"
        " may become dangerous and must not be consumed. "
        "It will be computed on the lot/serial number.",
        compute="_compute_date_fields",
    )
    use_time = fields.Integer(
        string="Product Use Time",
        help="Number of days before the goods starts deteriorating, "
        "without being dangerous yet."
        " It will be computed using the lot/serial number.",
        compute="_compute_date_fields",
    )
    removal_time = fields.Integer(
        string="Product Removal Time",
        help="Number of days before the goods should be removed from the stock. "
        "It will be computed on the lot/serial number.",
        compute="_compute_date_fields",
    )
    alert_time = fields.Integer(
        string="Product Alert Time",
        help="Number of days before an alert should be raised "
        "on the lot/serial number.",
        compute="_compute_date_fields",
    )

    specific_life_time = fields.Integer(
        string="Specific Product Life Time",
        help="Number of days before the goods may become dangerous "
        "and must not be consumed. "
        "It will be computed on the lot/serial number."
        " If not provided, the one defined on the parent is used.",
    )
    specific_use_time = fields.Integer(
        string="Specific Product Use Time",
        help="Number of days before the goods starts deteriorating, "
        "without being dangerous yet. "
        "It will be computed using the lot/serial number."
        " If not provided, the one defined on the parent is used.",
    )
    specific_removal_time = fields.Integer(
        string="Specific Product Removal Time",
        help="Number of days before the goods should be removed from the stock."
        " It will be computed on the lot/serial number."
        " If not provided, the one defined on the parent is used.",
    )
    specific_alert_time = fields.Integer(
        string="Specific Product Alert Time",
        help="Number of days before an alert should be raised on the lot/serial number."
        " If not provided, the one defined on the parent is used.",
    )

    parent_life_time = fields.Integer(
        string="Parent Product Life Time",
        help="Number of days before the goods may become dangerous and must not be consumed. "
        "It will be computed on the lot/serial number.",
        compute="_compute_parent_date_fields",
    )
    parent_use_time = fields.Integer(
        string="Parent Product Use Time",
        help="Number of days before the goods starts deteriorating,"
        " without being dangerous yet. "
        "It will be computed using the lot/serial number.",
        compute="_compute_parent_date_fields",
    )
    parent_removal_time = fields.Integer(
        string="Parent Product Removal Time",
        help="Number of days before the goods should be removed from the stock. "
        "It will be computed on the lot/serial number.",
        compute="_compute_parent_date_fields",
    )
    parent_alert_time = fields.Integer(
        string="Parent Product Alert Time",
        help="Number of days before an alert should be raised on the lot/serial number.",
        compute="_compute_parent_date_fields",
    )

    @api.depends("specific_compute_dates_from", "parent_compute_dates_from")
    def _compute_compute_dates_from(self):
        for rec in self:
            rec.compute_dates_from = (
                rec.specific_compute_dates_from
                or rec.parent_compute_dates_from
                or "current_date"
            )

    @api.depends(
        "parent_id.specific_compute_dates_from", "parent_id.parent_compute_dates_from"
    )
    def _compute_parent_compute_dates_from(self):
        for rec in self:
            parent_id = rec.parent_id
            rec.parent_compute_dates_from = (
                parent_id.specific_compute_dates_from
                or parent_id.parent_compute_dates_from
            )

    def _get_date_fields(self):
        return ["life_time", "use_time", "removal_time", "alert_time"]

    def _get_specific_and_parent_date_fields(self):
        specific_dates = ["specific_%s" % date for date in self._get_date_fields()]
        parent_dates = ["parent_%s" % date for date in self._get_date_fields()]
        return specific_dates + parent_dates

    @api.depends(lambda r: r._get_specific_and_parent_date_fields())
    def _compute_date_fields(self):
        for rec in self:
            for date in rec._get_date_fields():
                specific_value = getattr(rec, "specific_%s" % date)
                parent_value = getattr(rec, "parent_%s" % date)
                setattr(rec, date, specific_value or parent_value)

    def _get_parent_specific_and_parent_date_fields(self):
        return [
            "parent_id.%s" % date_field
            for date_field in self._get_specific_and_parent_date_fields()
        ]

    @api.depends(lambda r: r._get_parent_specific_and_parent_date_fields())
    def _compute_parent_date_fields(self):
        for rec in self:
            for date in self._get_date_fields():
                parent_id = rec.parent_id
                specific_value = getattr(parent_id, "specific_%s" % date)
                parent_value = getattr(parent_id, "parent_%s" % date)
                setattr(rec, "parent_%s" % date, specific_value or parent_value)
