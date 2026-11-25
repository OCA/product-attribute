# Copyright 2026 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    product_groupby_attribute_sort = fields.Selection(
        selection=[
            ("sequence", "Sequence"),
            ("name", "Name"),
        ],
        string="Attribute Group By Sort Order",
        default="sequence",
        required=True,
    )
