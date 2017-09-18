# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, tools
from odoo.modules.module import get_module_resource

from ..image_constants import (
    NONE,
    GLOBAL,
    CATEGORY,
    GLOBAL_CATEGORY,
)


class ResCompany(models.Model):

    _name = 'res.company'
    _description = 'ResCompany'
    _inherit = ['res.company', 'abstract.product.image']

    product_image_target = fields.Selection(
        string='Default Product Image',
        selection=[
            (NONE, 'No Default Image'),
            (GLOBAL, 'Global Product Image'),
            (CATEGORY, "Category's Image"),
            (GLOBAL_CATEGORY, 'Global and Category'),
        ],
        required=True,
        default='none',
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
        default=lambda s: s._default_product_image(),
        help='Use as the global image for all product default images. '
             'Limited to 1024x1024.',
    )

    @api.model
    def _default_product_image(self):
        image_path = get_module_resource(
            'product_default_image', 'static/src/img', 'glob_prod_img.png'
        )
        with open(image_path, 'rb') as handler:
            image_data = handler.read()
        return tools.image_resize_image_big(
            image_data.encode('base64')
        )

    @api.multi
    def write(self, vals):
        """ Changes product images if target or product_image have changed """

        target = vals.get('product_image_target')

        # Returns 0: field not present in vals.
        # Returns False: field present but image is False.
        product_image = vals.get('product_image', 0)

        if product_image is None and not target:
            return super(ResCompany, self).write(vals)

        tmpl_mod = self.env['product.template']

        if product_image:
            vals['product_image'] = \
                tools.image_resize_image_big(
                    base64_source=vals['product_image'],
                )
            product_image = vals['product_image']

        for record in self:

            old_target = record.product_image_target
            old_image = record.product_image

            # Default values for
            # NONE, GLOBAL, CATEGORY targets
            img_args = {
                'from_types': [
                    NONE, GLOBAL, CATEGORY,
                ],
                'company': record,
                'to_type': target,
                'to_img_bg': None,
                'in_cache': False,
                'add_domain': None,
            }

            available = (
                target and target != old_target,
                product_image != 0 and product_image != old_image,
            )

            if not any(available):
                continue

            # All or only target available
            elif all(available) or available[0]:

                if target == GLOBAL_CATEGORY:

                    img_args.update({
                        'to_type': CATEGORY,
                        'add_domain': [('categ_id.image', '!=', False)],
                    })

                    tmpl_mod._search_templates_change_images(**img_args)

                    img_args.update({
                        'to_type': GLOBAL,
                        'add_domain': [('categ_id.image', '=', False)],
                    })

                if all(available) and target in (GLOBAL, GLOBAL_CATEGORY):
                    img_args['to_img_bg'] = product_image

                tmpl_mod._search_templates_change_images(**img_args)

            # Image only available
            elif available[1]:

                target = old_target

                if target == GLOBAL_CATEGORY:
                    img_args['add_domain'] = [('categ_id.image', '=', False)]

                if target in (GLOBAL, GLOBAL_CATEGORY):
                    img_args.update({
                        'to_img_bg': product_image,
                        'to_type': GLOBAL,
                        'from_types': [GLOBAL, NONE],
                    })
                    tmpl_mod._search_templates_change_images(**img_args)

        return super(ResCompany, self).write(vals)
