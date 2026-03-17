# Copyright 2026 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_groupby_attribute_sort = fields.Selection(
        related="company_id.product_groupby_attribute_sort",
        string="Attribute Group By Sort Order",
        readonly=False,
        help="Defines the sort order applied to attribute values "
        "when grouping products by attribute in the searchbar.\n"
        "- Sequence: values are sorted by their sequence field.\n"
        "- Name: values are sorted alphabetically.",
    )
