# Copyright 2023 Komit - Cuong Nguyen Mtm
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    display_name = fields.Char(
        automatic=True,
        compute="_compute_display_name",
        search="_search_display_name",
    )

    def _search_display_name(self, operator, value):
        recs = (
            self.with_context(active_test=False)
            .search([])
            .filtered_domain([("display_name", operator, value)])
        )
        return [("id", "in", recs.ids)]
