# -*- coding: utf-8 -*-
# Copyright 2017 Graeme Gellatly
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import itertools
import psycopg2

from odoo import api, models
from odoo import tools
from odoo.exceptions import except_orm


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.multi
    def create_variant_ids(self):
        res = super(ProductTemplate, self).create_variant_ids()
        exclusion_obj = self.env['product.attribute.exclude']
        product_obj = self.env['product.product']
        for template in self:
            exclusion_values = exclusion_obj.search(
                ['|',
                 ('product_tmpl_ids', '=', template.id),
                 ('product_tmpl_ids', 'in', [])]
            )

            excl_attr_val_ids = exclusion_values.read(['attribute_value_ids'])
            excl_attr_val_ids = list(set(itertools.chain.from_iterable(
                [x.get('attribute_value_ids', []) for x in excl_attr_val_ids]
            )))

            products = product_obj.search([
                ('product_tmpl_id', '=', template.id),
                ('attribute_value_ids', 'in', excl_attr_val_ids)])

            variants_to_unlink = products.filtered(
                lambda p: any([e.attribute_value_ids <= p.attribute_value_ids
                               for e in exclusion_values]))

            variants_to_deactivate = []
            for variant in variants_to_unlink:
                try:
                    with self._cr.savepoint(), tools.mute_logger(
                            'odoo.sql_db'):
                        variant.unlink()
                # We catch all kind of exception to be sure that the operation
                # doesn't fail.
                except (psycopg2.Error, except_orm):
                    variants_to_deactivate.append(variant.id)
                    pass
            if variants_to_deactivate:
                product_obj.write(variants_to_deactivate, {'active': False})
        return res
