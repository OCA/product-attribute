# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import base64

from odoo import api, fields, models, tools
from odoo.modules.module import get_module_resource

from ..image_constants import CATEGORY, GLOBAL, GLOBAL_CATEGORY, NONE


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
            base64.b64encode(image_data)
        )

    @api.multi
    def write(self, vals):
        """ Changes product images if target or product_image have changed """

        target = vals.get('product_image_target')

        if 'product_image' not in vals and not target:
            return super(ResCompany, self).write(vals)

        if 'product_image' in vals:
            if isinstance(vals['product_image'], str):
                product_image = vals['product_image'].encode('ASCII')
            else:
                product_image = vals['product_image']
            vals['product_image'] = \
                tools.image_resize_image_big(
                    base64_source=product_image,
            )

        img_args = {
            'from_types': [
                NONE, GLOBAL, CATEGORY,
            ],
            'to_type': target,
            'to_img_bg': None,
            'in_cache': False,
            'add_domain': None,
            'company': None,
        }

        if 'product_image' in vals and target not in (NONE, CATEGORY):

            img_args['to_img_bg'] = vals['product_image']

            if not target:
                img_args.update({
                    'from_types': [GLOBAL],
                    'to_type': GLOBAL,
                })

        tmpl_mod = self.env['product.template']

        if target == GLOBAL_CATEGORY:

            img_args.update({
                'add_domain': [('categ_id.image', '!=', False)],
                'to_type': CATEGORY,
            })

            for record in self:
                img_args['company'] = record
                tmpl_mod._search_templates_change_images(**img_args)

            img_args.update({
                'add_domain': [('categ_id.image', '=', False)],
                'to_type': GLOBAL,
            })

        for record in self:
            img_args['company'] = record
            tmpl_mod._search_templates_change_images(**img_args)

        return super(ResCompany, self).write(vals)
