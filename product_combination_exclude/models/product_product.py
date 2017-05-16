# -*- coding: utf-8 -*-
# Copyright 2017 Graeme Gellatly
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, models


_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):

    _inherit = 'product.product'

    @api.multi
    def create(self, vals):

        if 'attribute_value_ids' not in vals:
            return super(ProductProduct, self).create(vals)

        exclusion_obj = self.env['product.attribute.exclude']
        search_args = []

        if 'product_tmpl_id' in vals:
            search_args += [
                '|',
                ('product_tmpl_ids', 'in', [vals['product_tmpl_id']]),
                ('product_tmpl_ids', 'in', []),
            ]

        attribute_ids = []

        for attr_line in vals['attribute_value_ids']:
            try:
                attribute_ids += attr_line[2]
            except IndexError:
                attribute_ids.append(attr_line[1])

        if not attribute_ids:
            return super(ProductProduct, self).create(vals)

        search_args += [
            ('attribute_value_ids', 'in', attribute_ids),
        ]
        attr_values = self.env['product.attribute.value'].browse(
            attribute_ids
        )
        exclusion_values = exclusion_obj.search(search_args)

        for excl_val in exclusion_values:
            if excl_val.attribute_value_ids <= attr_values:
                return self.browse()

        return super(ProductProduct, self).create(vals)
