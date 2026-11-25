# Copyright 2026 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    exclude_from_groupby = fields.Boolean(
        string="Exclude from Group By",
        default=False,
        help="If checked, this attribute will not appear in the "
        " 'Group by attribute' search menu.",
    )
