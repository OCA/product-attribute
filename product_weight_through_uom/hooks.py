# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry, vals=None):
    """For brand new installations"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Change only those with no weight already set
    products_init = env['product.product'].search([
        ('is_weight_uom', '=', True),
        ('weight', '=', 0),
    ])
    for product in products_init:
        product._onchange_uom()
