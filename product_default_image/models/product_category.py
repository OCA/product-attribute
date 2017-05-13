# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, tools


class ProductCategory(models.Model):

    _inherit = 'product.category'

    image = fields.Binary(
        string='Image',
        attachment=True,
        help='This field holds the image used for the category, '
             'limited to 1024x1024px. Also used as the default '
             'image for products of this category.',
    )
    image_medium = fields.Binary(
        string='Medium-Sized Image',
        attachment=True,
        help='Medium-sized image of the category. It is automatically '
             'resized as a 128x128px image, with aspect ratio preserved, '
             'only when the image exceeds one of those sizes. '
             'Use this field in form views or some kanban views.',
    )
    image_small = fields.Binary(
        string='Small-Sized Image',
        attachment=True,
        help='Small-sized image of the category. It is automatically '
             'resized as a 64x64px image, with aspect ratio preserved. '
             'Use this field anywhere a small image is required.',
    )

    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(ProductCategory, self).create(vals)

    @api.multi
    def write(self, vals):

        tools.image_resize_images(vals)
        target = self.env.user.company_id.product_image_target

        if target not in ['category', 'global_category']:
            return super(ProductCategory, self).write(vals)

        keys = ['image', 'image_medium', 'image_small']
        imgs_present = [vals[key] for key in keys if key in vals]

        if not imgs_present:
            return super(ProductCategory, self).write(vals)

        img_args = {
            'from_types': ['default_category', 'no_image'],
            'to_type': 'default_category',
            'to_img_bg': imgs_present[0],
            'add_domain': [('categ_id', 'in', self.ids)],
        }

        if target == 'category' and not imgs_present[0]:
            img_args.update({
                'to_type': 'no_image',
                'to_img_bg': None,
            })

        if target == 'global_category':
            img_args['from_types'] += ['default_global']
            if not imgs_present[0]:
                img_args.update({
                    'to_type': 'default_global',
                    'to_img_bg': None,
                })

        self.env['product.template'].search_change_images(**img_args)
        return super(ProductCategory, self).write(vals)
