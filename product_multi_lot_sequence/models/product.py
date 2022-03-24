# Copyright 2022 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_lot_sequence_ids = fields.One2many(
        "product.lot.sequence",
        "product_tmpl_id",
        string="Product Lot Sequence",
        help="This field contains the information related to the " "numbering of lots.",
        copy=False,
    )
