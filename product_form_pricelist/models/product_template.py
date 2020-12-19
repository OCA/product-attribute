# Copyright 2020 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    fixed_pricelist_item_ids = fields.One2many(
        "product.pricelist.item", "product_tmpl_id", "Fixed Pricelist Items"
    )
