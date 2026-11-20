# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    manufactured_for_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="product_product_manuf_for_partner_rel",
        column1="product_id",
        column2="partner_id",
        domain=["|", ("customer_rank", ">", 0), ("is_company", "=", True)],
        string="Manufactured for",
    )
