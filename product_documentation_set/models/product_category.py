# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):

    _inherit = "product.category"

    doc_set_ids = fields.Many2many(
        "product.doc.set",
        string="Documentation Sets",
        help="Sets of product documentation, to use for several purposes. "
        "Specific sets may be defined by country or language.",
    )
