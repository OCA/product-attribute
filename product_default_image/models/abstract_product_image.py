# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, models

from ..image_constants import IMAGE_FIELDS


class AbstractProductImage(models.AbstractModel):

    _name = 'abstract.product.image'
    _description = 'Abstract Product Image'

    @api.model
    def _vals_get_images(self, vals,
                         false_filter=False, img_keys=IMAGE_FIELDS):
        """ Returns images from given vals argument.

        Args:
            vals (dict): Dictionary containing the image fields.

            false_filter (bool): Set True if wanting to filter out
                any False image values.

            img_keys (list, tuple, str): Contains string values of image
                fields. If specifying multiple, use a list or tuple.

        Returns:
            list: Returns image values of the img_keys in the vals arg
                if the keys are in the vals dict.

        """
        if not isinstance(img_keys, (list, tuple)):
            img_keys = (img_keys,)

        img_vals = [
            vals[key] for key in img_keys if key in vals
        ]
        if false_filter:
            img_vals = list(filter(None, img_vals))

        return img_vals

    @api.multi
    def _get_images(self, false_filter=False, img_keys=IMAGE_FIELDS):
        self.ensure_one()
        return self._vals_get_images(self.read()[0], false_filter, img_keys)
