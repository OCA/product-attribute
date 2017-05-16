# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, SUPERUSER_ID


def _trigger_onchange_price_discount(cr, registry):
    with cr.savepoint():
        env = api.Environment(cr, SUPERUSER_ID, {})
        pricelist_item_mod = env['product.pricelist.item']
        items = pricelist_item_mod.search([('compute_price', '=', 'tiered')])

        for item in items:
            item._onchange_price_discount()
