# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, SUPERUSER_ID

from .image_constants import CUSTOM


def find_templates_with_imgs(cr, registry):
    with cr.savepoint():
        env = api.Environment(cr, SUPERUSER_ID, {})
        ProductTemplate = env['product.template']
        if ProductTemplate._fields['image'].store:
            tmpls = ProductTemplate.search([
                ('image', '!=', False),
            ])
        else:
            # some modules (like product_multi_image) could change image to
            # non-store, so it is necessary to get all product templates and
            # filter them
            tmpls = ProductTemplate.search([])
            tmpls = tmpls.filtered(lambda tmpl: tmpl.image)
        tmpls.write({
            'image_type': CUSTOM,
        })
