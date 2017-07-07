# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, SUPERUSER_ID

from .image_constants import CUSTOM


def find_templates_with_imgs(cr, registry):
    with cr.savepoint():
        env = api.Environment(cr, SUPERUSER_ID, {})
        tmpls = env['product.template'].search([
            ('image', '!=', False),
        ])
        tmpls.write({
            'image_type': CUSTOM,
        })
