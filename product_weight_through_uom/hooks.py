# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry, vals=None):
    """For brand new installations"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Change only those with no weight already set
    products_init = env['product.product'].search([
        ('weight', '=', 0),
    ]).filtered('is_weight_uom')
    for product in products_init:
        product._onchange_uom_product_weight_through_uom()
