# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, models

from ..image_constants import TYPES, TARGETS


class AbstractProductImage(models.AbstractModel):

    _name = 'abstract.product.image'
    _description = 'Abstract Product Image'

    @api.model
    def _vals_get_images(self, vals,
                         img_keys=('image', 'image_medium', 'image_small')):

        img_keys = self._ensure_iterable_arg(img_keys)
        return [vals[key] for key in img_keys if key in vals]

    @api.multi
    def _get_images(self,
                    img_keys=('image', 'image_medium', 'image_small')):

        self.ensure_one()
        img_keys = self._ensure_iterable_arg(img_keys)
        return [getattr(self, key) for key in img_keys]

    @api.model
    def _target_match_any(self, target_val, targets_keys):
        return self._val_match_any(
            target_val, TARGETS, targets_keys
        )

    @api.model
    def _type_match_any(self, type_val, types_keys):
        return self._val_match_any(
            type_val, TYPES, types_keys
        )

    @api.model
    def _val_match_any(self, val, source_dict, source_dict_keys):
        source_dict_keys = self._ensure_iterable_arg(
            source_dict_keys
        )
        for key in source_dict_keys:
            if val == source_dict.get(key, False):
                return True

    @api.model
    def _ensure_iterable_arg(self, arg):
        if not isinstance(arg, (list, tuple)):
            arg = [arg]
        return arg
