# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, tools
from odoo.modules.module import get_module_resource


class ResCompany(models.Model):

    _inherit = 'res.company'

    product_image_target = fields.Selection(
        string='Default Product Image',
        selection=[
            ('none', 'No Default Image'),
            ('global', 'Global Product Image'),
            ('category', "Category's Image"),
            ('global_category', 'Global and Category'),
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
        return tools.image_resize_image_big(
            open(image_path, 'rb').read().encode('base64')
        )

    @api.multi
    def write(self, vals):
        """ Changes product images if target has changed

        Examples:

            * In examples 1 and 2, product.template images
              will not be updated with the new some_image
              value.

            * Examples 3 and 4 will ensure product.template images
              are updated to the new some_image value.

            .. code-block:: python

            # 1
            company.write({
                'product_image': some_image,
            })

            # 2
            company.product_image_target = 'global'
            company.product_image = some_image

            # 3
            company.write({
                'product_image': some_image,
                'product_image_target': 'global',
            })

            # 4
            company.product_image = some_image
            company.product_image_target = 'global'

        """
        target = vals.get('product_image_target')

        if 'product_image' not in vals and not target:
            return super(ResCompany, self).write(vals)

        if 'product_image' in vals:
            vals['product_image'] = \
                tools.image_resize_image_big(
                    base64_source=vals['product_image'],
                )

        target_map = {
            'none': 'no_image',
            'category': 'default_category',
            'global': 'default_global',
            'global_category': 'default_category',
        }

        if target not in target_map:
            return super(ResCompany, self).write(vals)

        img_args = {
            'from_types': [
                'no_image', 'default_global', 'default_category'
            ],
            'to_type': target_map[target],
            'to_img_bg': None,
            'in_cache': False,
            'add_domain': None,
        }

        if 'product_image' in vals:
            img_args['to_img_bg'] = vals['product_image']

        tmpl_mod = self.env['product.template']

        if target == 'global_category':
            img_args['add_domain'] = [('categ_id.image', '!=', False)]
            tmpl_mod.search_change_images(**img_args)
            img_args.update({
                'add_domain': [('categ_id.image', '=', False)],
                'to_type': 'default_global',
            })

        tmpl_mod.search_change_images(**img_args)
        return super(ResCompany, self).write(vals)
