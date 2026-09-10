# Copyright 2023 Akretion (https://www.akretion.com).
# @author Raphaël Reverdy<raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    description_sale_short = fields.Text(
        "Sales Description Short",
        translate=True,
        help="A short description of the Product that"
        " you want to communicate to your customers. ",
    )
    description_sale_long = fields.Html(
        "Sales Description Long",
        translate=True,
        help="A long description of the Product that"
        " you want to communicate to your customers. ",
    )
