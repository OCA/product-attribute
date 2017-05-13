# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from collections import defaultdict

from odoo import api, fields, models, tools


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    auto_change_image = fields.Boolean(
        string='Auto Change Image',
        default=True,
        help='Allow/disallow automatic changes to product image. '
             'Uncheck to stop being changed to a default image.',
    )
    img_type = fields.Selection(
        string='Image Type',
        selection=[
            ('default_global', 'Global'),
            ('default_category', 'Category'),
            ('no_image', 'No Image'),
            ('custom', 'Custom'),
        ],
        required=True,
        readonly=True,
        default='no_image',
    )

    @api.model
    def default_get(self, vals):

        vals = super(ProductTemplate, self).default_get(vals)

        company = self.env.user.company_id
        target = company.product_image_target

        if target in ['category', 'global_category'] and vals.get('categ_id'):
            categ = self.env['product.category'].browse(vals['categ_id'])
            vals.update({
                'image': categ.image,
                'img_type': 'default_category',
            })

        if target in ['global', 'global_category'] and not vals.get('image'):
            vals.update({
                'image': company.product_image,
                'img_type': 'default_global',
            })

        tools.image_resize_images(vals)
        return vals

    @api.model
    def search_change_images(self, from_types, to_type, to_img_bg=None,
                             add_domain=None, in_cache=False):

        templates = self.search_by_img_types(
            from_types=from_types,
            add_domain=add_domain,
        )

        if not templates:
            return

        img_args = {
            'to_type': to_type,
            'in_cache': in_cache,
        }
        if to_img_bg:
            img_args['to_img_bg'] = to_img_bg

        return templates.change_template_image(**img_args)

    @api.model
    def search_by_img_types(self, from_types, add_domain=None):
        """ Constructs domain and searches using from_types, add_domain

            Args:
                from_types:
                    List of selections from img_type field to search
                    products by.

                add_domain:
                    If you wish to add domain items to the method's default
                    ones, use this parameter to do so. Must be a list.

            Example:
                .. code-block:: python

                templates = self.env['product.template'].search_by_img_types(
                    from_types=['default_category', 'no_image'],
                    add_domain=[('categ_id', '=', record.id)],
                )

            Returns:
                The above example will return a recordset using a domain of:
                    .. code-block:: python

                    [
                        ('company_id', '=', some_id_int),
                        ('auto_change_image', '=', True),
                        ('img_type', 'in', ['default_category',
                                              'no_image']),
                        ('categ_id', '=', some_id_int),
                    ]

        """
        if not add_domain:
            add_domain = []

        if not isinstance(from_types, list):
            raise TypeError('from_types argument must be a list')

        if add_domain and not isinstance(add_domain, list):
            raise TypeError('add_domain argument must be a list')

        domain = [
            ('company_id', '=', self.env.user.company_id.id),
            ('auto_change_image', '=', True),
            ('img_type', 'in', from_types),
        ]
        domain += add_domain
        return self.search(domain)

    @api.multi
    @api.onchange('categ_id')
    def _onchange_categ_id(self):

        company = self.env.user.company_id
        target = company.product_image_target

        if target not in ['category', 'global_category']:
            return

        for record in self:

            if not record.auto_change_image:
                continue

            if record.img_type == 'custom':
                continue

            categ = record.categ_id

            img_args = {
                'to_type': 'default_category',
                'in_cache': True,
            }
            if not categ.image and target == 'global_category':
                img_args['to_type'] = 'default_global'

            record.change_template_image(**img_args)

    @api.multi
    def change_template_image(self, to_type, to_img_bg=None, in_cache=False):
        """ Change product template image to specified to_type's image
            or to_img_bg.

            Args:
                to_type:
                    Value specified allowed from img_type field which the
                    image should be targeted to. Accepted values are:

                        'default_global'
                            * product_image field defined in res.company

                        'default_category',
                            * product's categ_id field's image

                        'no_image'
                            * Deletes the image

                        'custom'
                            * Set to the image you specify using to_img_bg.
                            Note that targeting to custom will prevent the
                            image from automatically being changed in the
                            future until deleted or manually re-mapped to a
                            default image.

                to_img:
                    Can be used as an override if the template
                    images should be changed to a specific image.
                    Image is resized to image big value and scaled
                    down to medium and small values.

                    Note that to_type is required even if to_img_bg
                    arg is supplied.

                in_cache:
                    Set True if calling this method to change the images
                    in cache (helpful when calling from an onchange method
                    in product.template)

            Returns:
                recordset if tmpl images have been changed.

                None/False if any of below conditions are True.

        """
        if any([
                to_type not in [
                    'default_global', 'default_category',
                    'no_image', 'custom'],
                to_type == 'custom' and not to_img_bg,
                to_type == 'no_image' and to_img_bg,
                not isinstance(in_cache, bool)]):
            return

        # {img_bg: records}
        write_map = defaultdict(lambda: self.env['product.template'].browse())

        if to_img_bg:
            to_img_bg = tools.image_resize_image_big(to_img_bg)
            write_map[to_img_bg] += self

        elif to_type == 'no_image':
            write_map[None] += self

        elif to_type == 'default_global':
            company = self.env.user.company_id
            write_map[company.product_image] += self

        elif to_type == 'default_category':
            for record in self:
                write_map[record.categ_id.image] += record

        if in_cache:

            for img_bg, records in write_map.iteritems():

                img_md = tools.image_resize_image_medium(img_bg)
                img_sm = tools.image_resize_image_small(img_bg)

                for record in records:
                    record.image = img_bg
                    record.image_medium = img_md
                    record.image_small = img_sm
                    record.img_type = to_type

        else:

            for img_bg, records in write_map.iteritems():

                for record in records:
                    record.write({
                        'image': img_bg,
                        'img_type': to_type,
                    })
                # records.write({
                #     'image': img_bg,
                #     'img_type': to_type,
                # })

        return self

    @api.multi
    def apply_default_image(self):

        self.ensure_one()
        target = self.env.user.company_id.product_image_target
        self.auto_change_image = True

        to_keys = {
            'none': 'no_image',
            'global': 'default_global',
            'category': 'default_category',
            'global_category': 'default_category',
        }

        if target not in to_keys:
            return

        if target == 'global_category':
            categ = self.categ_id
            if not any([categ.image, categ.image_medium, categ.image_small]):
                to_keys['global_category'] = 'default_global'

        self.change_template_image(
            to_type=to_keys[target],
        )

    @api.multi
    def write(self, vals):

        keys = ['image', 'image_medium', 'image_small']
        imgs_present = [vals[key] for key in keys if key in vals]

        if imgs_present:
            if not imgs_present[0]:
                vals['img_type'] = 'no_image'

            if imgs_present[0] and not vals.get('img_type'):
                vals['img_type'] = 'custom'

        return super(ProductTemplate, self).write(vals)
