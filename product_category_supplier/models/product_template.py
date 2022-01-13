# Copyright (C) 2022 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    supplier_categ_id = fields.Many2one(
        comodel_name="product.category",
        string="Supplier Category",
        domain="[('type', '=', 'supplier')]",
    )
