# -*- coding: utf-8 -*-

from . import models

from openerp import api, SUPERUSER_ID


def post_init_hook(cr, pool):
    """Update list price with taxes include for all products.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    products = env['product.template'].search([])
    for product in products:
        product.list_price_tax = product.list_price * (
            product._get_factor_tax(product.taxes_id))
