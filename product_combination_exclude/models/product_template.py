# -*- coding: utf-8 -*-
# Copyright 2017 Graeme Gellatly
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import itertools
import psycopg2

from odoo import api, models
from odoo import tools
from odoo.exceptions import except_orm


_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.multi
    def create_variant_ids(self):
        res = super(ProductTemplate, self).create_variant_ids()
        exclusion_obj = self.env['product.attribute.exclude']
        product_obj = self.env['product.product']
        for template in self:
            exclusion_values = exclusion_obj.search([
                 ('product_tmpl_ids', 'in', template.ids),
            ])

            excl_attr_vals = exclusion_values.mapped('attribute_value_ids')

            products = product_obj.search([
                ('product_tmpl_id', '=', template.id),
                ('attribute_value_ids', 'in', excl_attr_vals.ids),
            ])

            variants_to_unlink = products.filtered(
                lambda p: any([e.attribute_value_ids <= p.excl_attr_vals
                               for e in exclusion_values])
            )

            variants_to_deactivate = product_obj.browse()
            for variant in variants_to_unlink:
                try:
                    with self._cr.savepoint(), tools.mute_logger(
                            'odoo.sql_db'):
                        variant.unlink()
                # We catch all kind of exception to be sure that the operation
                # doesn't fail.
                except (psycopg2.Error, except_orm):
                    variants_to_deactivate += variant
            if variants_to_deactivate:
                variants_to_deactivate.write({'active': False})
        return res
