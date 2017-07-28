# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class StockConfigSettings(models.TransientModel):

    _inherit = 'stock.config.settings'

    product_image_target = fields.Selection(
        string='Default Product Image',
        related='company_id.product_image_target',
        required=True,
        help='Determines the type of default images to use. '
             'Changing this field will set all empty product images '
             'to the target you specify. Products with a default image '
             'from the previous target are changed to your new target '
             'as well.\n\n'
             'No Default Image: Deletes images.\n\n'
             'Global: Set to Global Product Image.\n\n'
             'Category: Set products to their category image.\n\n'
             'Global and Category: Set products to their category '
             'image if the category has an image. Otherwise set it to '
             'the Global Product Image',
    )
    product_image = fields.Binary(
        string='Global Product Image',
        related='company_id.product_image',
        required=True,
        help='Use as the global image for all product default images. '
             'Limited to 1024x1024.',
    )
