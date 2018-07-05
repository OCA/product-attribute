# -*- coding: utf-8 -*-
# © 2014-2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = [_name, "base_multi_image.owner"]

    image = fields.Binary(
        related='image_main',
        store=False,
    )
    image_medium = fields.Binary(
        related='image_main_medium',
        store=False,
    )
    image_small = fields.Binary(
        related='image_main_small',
        store=False,
    )

    @api.multi
    def write(self, vals):
        if set(['image', 'image_medium', 'image_small']) & set(vals.keys()):
            # medium/small image is saved as large
            # on load image will be medium/small resized on the fly
            if 'image' in vals:
                pass
            elif 'image_medium' in vals:
                vals['image'] = vals['image_medium']
                del vals['image_medium']
            elif 'image_small' in vals:
                vals['image'] = vals['image_small']
                del vals['image_small']
        return super(ProductTemplate, self).write(vals)

    @api.multi
    def _set_multi_image_main_medium(self):
        # on save product module resizes large image to medium
        # medium image should not overwrite the large
        pass

    @api.multi
    def _set_multi_image_main_small(self):
        # on save product module resizes large image to small
        # small image should not overwrite the large
        pass
