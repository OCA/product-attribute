# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from collections import defaultdict

from odoo import api, fields, models, tools

from ..image_constants import TYPES, TARGETS


class ProductTemplate(models.Model):

    _name = 'product.template'
    _description = 'Product Template'
    _inherit = ['product.template', 'abstract.product.image']

    auto_change_image = fields.Boolean(
        string='Auto Change Image',
        default=True,
        help='Allow/disallow automatic changes to product image. '
             'Uncheck to stop being changed to a default image.',
    )
    image_type = fields.Selection(
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
    product_image_target = fields.Selection(
        string='Default Product Image',
        related='company_id.product_image_target',
        required=True,
    )

    @api.model
    def default_get(self, vals):

        vals = super(ProductTemplate, self).default_get(vals)

        company = self.env.user.company_id
        target = company.product_image_target

        if self._target_match_any(target, (2, 3)) \
                and vals.get('categ_id'):

            categ = self.env['product.category'].browse(vals['categ_id'])
            vals.update({
                'image': categ.image,
                'image_type': TYPES[1],
            })

        if self._target_match_any(target, (1, 3)) \
                and not any(self._vals_get_images(vals)):

            vals.update({
                'image': company.product_image,
                'image_type': TYPES[0],
            })

        tools.image_resize_images(vals)
        return vals

    @api.model
    def _search_templates_change_images(
            self, from_types, to_type, to_img_bg=None,
            add_domain=None, in_cache=False):
        """ Wraps _search_by_image_types and _change_template_image
            into one method.

        """
        templates = self._search_by_image_types(
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

        return templates._change_template_image(**img_args)

    @api.model
    def _search_by_image_types(self, from_types, add_domain=None):
        """ Constructs domain and searches using from_types, add_domain

            Args:
                from_types (list): List of selections from image_type
                    field to search products by.

                add_domain (list): If you wish to add domain items to
                    the method's default ones, use this parameter to
                    do so. Must be a list.

            Example:
                .. code-block:: python

                Product = self.env['product.template']
                templates = Product._search_by_image_types(
                    from_types=[TYPES[1], TYPES[2]],
                    add_domain=[('categ_id', '=', record.id)],
                )

                The above example will return a recordset using a domain of:

                    .. code-block:: python

                    [
                        ('company_id', '=', some_id_int),
                        ('auto_change_image', '=', True),
                        ('image_type', 'in', [TYPES[1], TYPES[2]]),
                        ('categ_id', '=', some_id_int),
                    ]

            Returns:
                ProductTemplate: Recordset using the following domain:

                    .. code-block:: python

                    [
                        ('company_id', '=', some_id_int),
                        ('auto_change_image', '=', True),
                        ('image_type', 'in', from_types arg),
                    ]

                    You can add additional domain items using the add_domain
                    arg, which will be appended to the above constructed
                    domain.

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
            ('image_type', 'in', from_types),
        ]
        domain += add_domain
        return self.search(domain)

    @api.multi
    @api.onchange('categ_id')
    def _onchange_categ_id(self):

        company = self.env.user.company_id
        target = company.product_image_target

        if self._target_match_any(target, (0, 1)):
            return

        for record in self:

            if not record.auto_change_image:
                continue

            if self._type_match_any(record.image_type, 3):
                continue

            categ = record.categ_id

            img_args = {
                'to_type': TYPES[1],
                'in_cache': True,
            }
            if not categ.image and self._target_match_any(target, 3):
                img_args['to_type'] = TYPES[0]

            record._change_template_image(**img_args)

    @api.multi
    def _change_template_image(self, to_type, to_img_bg=None, in_cache=False):
        """ Change product template image to specified to_type's image
            or to_img_bg.

            Args:
                to_type (str): Value specified allowed from image_type field
                    which the image should be targeted to. Accepted values are:

                    global
                        * product_image field defined in res.company

                    category
                        * product's categ_id field's image

                    none
                        * Deletes the image

                    global_category
                        * Set to the image you specify using to_img_bg.
                        Note that targeting to custom will prevent the
                        image from automatically being changed in the
                        future until deleted or manually re-mapped to a
                        default image.

                to_img (base64): Can be used as an override if the template
                    images should be changed to a specific image.
                    Image is resized to image big value and scaled
                    down to medium and small values.

                    Note that to_type is required even if to_img_bg
                    arg is supplied.

                in_cache (bool): Set True if calling this method to change the
                    images in cache (helpful when calling from an onchange
                    method in product.template)

            Returns:
                ProductTemplate: Recordset if tmpl images have been changed.
                None: if any of the conditions below are True.

        """
        if any([
                to_type not in TYPES.values(),
                to_type == TYPES[3] and not to_img_bg,
                to_type == TYPES[2] and to_img_bg,
                not isinstance(in_cache, bool)]):
            return

        write_map = defaultdict(lambda: self.env['product.template'].browse())

        if to_img_bg:
            to_img_bg = tools.image_resize_image_big(to_img_bg)
            write_map[to_img_bg] += self

        elif to_type == TYPES[2]:
            write_map[None] += self

        elif to_type == TYPES[0]:
            company = self.env.user.company_id
            write_map[company.product_image] += self

        elif to_type == TYPES[1]:
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
                    record.image_type = to_type

        else:

            for img_bg, records in write_map.iteritems():

                # image only written to last or last few records
                # if writing directly on recordset
                for record in records:
                    record.write({
                        'image': img_bg,
                        'image_type': to_type,
                    })

        return self

    @api.multi
    def apply_default_image(self):

        self.ensure_one()
        target = self.env.user.company_id.product_image_target
        self.auto_change_image = True

        to_keys = {
            TARGETS[0]: TYPES[2],
            TARGETS[1]: TYPES[0],
            TARGETS[2]: TYPES[1],
            TARGETS[3]: TYPES[1],
        }

        if target not in to_keys:
            return

        if self._target_match_any(target, 3):
            if not any(self.categ_id._get_images()):
                to_keys[TARGETS[3]] = TYPES[0]

        self._change_template_image(
            to_type=to_keys[target],
        )

    @api.multi
    def write(self, vals):

        changed_images = self._vals_get_images(vals)

        if changed_images:
            if not changed_images[0]:
                vals['image_type'] = TYPES[2]

            if changed_images[0] and not vals.get('image_type'):
                vals['image_type'] = TYPES[3]

        return super(ProductTemplate, self).write(vals)
