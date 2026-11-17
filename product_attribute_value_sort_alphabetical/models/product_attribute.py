# Copyright (C) 2026 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    sort_alphabetically = fields.Boolean(
        string="Sort Values Alphabetically",
        help="Values sequence is automatically computed in alphabetical order.",
    )
    keep_manual_sort = fields.Boolean(
        help="Safety lock: freeze the current sequence of the values and allow "
        "to reorder them manually, even if the alphabetical sort is enabled.",
    )
    sort_field = fields.Selection(
        selection="_selection_sort_field",
        string="Sort Alphabetically On",
        default="name",
        required=True,
    )
    is_value_sequence_computed = fields.Boolean(
        compute="_compute_is_value_sequence_computed",
    )

    @api.model
    def _selection_sort_field(self):
        return [("name", self.env._("Name"))]

    @api.depends("sort_alphabetically", "keep_manual_sort")
    def _compute_is_value_sequence_computed(self):
        for record in self:
            record.is_value_sequence_computed = (
                record.sort_alphabetically and not record.keep_manual_sort
            )
