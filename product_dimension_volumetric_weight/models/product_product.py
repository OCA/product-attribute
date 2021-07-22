# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    volumetric_weight = fields.Float(
        string="Volumetric weight",
        related="product_tmpl_id.volumetric_weight",
        store=True,
        digits="Stock Weight",
    )
