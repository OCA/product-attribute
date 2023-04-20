# Copyright 2022 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductCategory(models.Model):

    _inherit = "product.category"

    # This is the // as Odoo core field in product model
    use_expiration_date = fields.Boolean(
        compute="_compute_use_expiration_date",
        store=True,
        readonly=False,
    )

    @api.depends("parent_id")
    def _compute_use_expiration_date(self):
        """
        Change the value of use_expiration_date field
        when parent
        """
        for category in self:
            category.use_expiration_date = category.parent_id.use_expiration_date

    expiration_time = fields.Integer(
        string="Product Expiration Time",
        help="Number of days before the goods"
        " may become dangerous and must not be consumed. "
        "It will be computed on the lot/serial number.",
        compute="_compute_date_fields",
        store=True,
        readonly=False,
        recursive=True,
    )
    use_time = fields.Integer(
        string="Product Use Time",
        help="Number of days before the goods starts deteriorating, "
        "without being dangerous yet."
        " It will be computed using the lot/serial number.",
        compute="_compute_date_fields",
        store=True,
        readonly=False,
        recursive=True,
    )
    alert_time = fields.Integer(
        string="Product Alert Time",
        help="Number of days before an alert should be raised "
        "on the lot/serial number.",
        compute="_compute_date_fields",
        store=True,
        readonly=False,
        recursive=True,
    )

    removal_time = fields.Integer(
        string="Product Removal Time",
        help="Number of days before an alert should be raised "
        "on the lot/serial number.",
        compute="_compute_date_fields",
        store=True,
        readonly=False,
        recursive=True,
    )

    @api.model
    def _get_date_fields(self):
        return ["expiration_time", "use_time", "removal_time", "alert_time"]

    @api.depends(lambda r: r._get_parent_specific_and_parent_date_fields())
    def _compute_date_fields(self):
        for rec in self:
            for date in rec._get_date_fields():
                parent_value = getattr(rec.parent_id, "%s" % date)
                value = getattr(rec, "%s" % date)
                setattr(rec, date, value or parent_value)

    def _get_parent_specific_and_parent_date_fields(self):
        return ["parent_id.%s" % date_field for date_field in self._get_date_fields()]
