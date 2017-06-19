# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, tools

from ..image_constants import TYPES


class ProductCategory(models.Model):

    _name = 'product.category'
    _description = 'Product Category'
    _inherit = ['abstract.product.image', 'product.category']

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
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(ProductCategory, self).create(vals)

    @api.multi
    def write(self, vals):

        tools.image_resize_images(vals)
        target = self.env.user.company_id.product_image_target

        if not self._target_match_any(target, (2, 3)):
            return super(ProductCategory, self).write(vals)

        changed_images = self._vals_get_images(vals)

        if not changed_images:
            return super(ProductCategory, self).write(vals)

        img_args = {
            'from_types': [TYPES[1], TYPES[2]],
            'to_type': TYPES[1],
            'to_img_bg': changed_images[0],
            'add_domain': [('categ_id', 'in', self.ids)],
        }

        if self._target_match_any(target, 2) and not changed_images[0]:
            img_args.update({
                'to_type': TYPES[2],
                'to_img_bg': None,
            })

        if self._target_match_any(target, 3):
            img_args['from_types'].append(TYPES[0])
            if not changed_images[0]:
                img_args.update({
                    'to_type': TYPES[0],
                    'to_img_bg': None,
                })

        self.env['product.template'].\
            _search_templates_change_images(**img_args)
        return super(ProductCategory, self).write(vals)
