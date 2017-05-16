# -*- coding: utf-8 -*-
# Copyright 2017 Graeme Gellatly
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import itertools
from collections import defaultdict

from odoo import api, fields, models


class ProductAttributeExcludeMatrix(models.Model):

    _name = 'product.attribute.exclude.matrix'
    _description = 'Product Attribute Exclusion Matrix'

    name = fields.Char(required=True)
    description = fields.Text()
    attribute_value_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        string='Incompatible Attributes',
    )
    product_tmpl_ids = fields.Many2many(
        comodel_name='product.template',
        string='Product Templates',
    )
    exclusion_line_ids = fields.One2many(
        comodel_name='product.attribute.exclude',
        inverse_name='matrix_id',
        string='Excluded Combinations',
    )

    @api.multi
    def button_generate_exclusions(self):
        self.ensure_one()

        delete_lines = [(2, line.id) for line in self.exclusion_line_ids]

        # Sort the list into a list of lists by its attribute
        grouped_attrs = itertools.groupby(self.attribute_value_ids,
                                          key=lambda x: x.attribute_id.id)
        grouped_attrs_dict = defaultdict(list)
        for k, v in grouped_attrs:
            grouped_attrs_dict[k].extend(list(v))
        grouped_attrs = grouped_attrs_dict.values()

        if len(grouped_attrs) <= 1:
            return True

        # Create the combinations and put into write format
        attribute_matrix = itertools.product(*grouped_attrs)
        exclusion_lines = [
            (0, 0,
             {'attribute_value_ids': [(6, 0, [v.id for v in am])],
              'product_tmpl_ids': [(6, 0, self.product_tmpl_ids.ids)]})
            for am in attribute_matrix
        ]

        self.write({'exclusion_line_ids': delete_lines + exclusion_lines})
        return True

    @api.multi
    def button_update_products(self):
        self.ensure_one()
        if not self.product_tmpl_ids:
            return
        self.product_tmpl_ids.create_variant_ids()
        return True
