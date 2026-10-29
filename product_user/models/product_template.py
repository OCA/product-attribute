# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Product Manager",
        domain=[("share", "=", False)],
    )
