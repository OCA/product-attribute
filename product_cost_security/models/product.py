# Copyright 2018 Sergio Teruel - Tecnativa <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    standard_price = fields.Float(groups="product_cost_security.group_product_cost")


class ProductProduct(models.Model):
    _inherit = "product.product"

    standard_price = fields.Float(groups="product_cost_security.group_product_cost")
