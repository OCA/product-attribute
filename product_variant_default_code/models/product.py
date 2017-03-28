# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import MissingError
import re
from string import Template
from collections import defaultdict

DEFAULT_REFERENCE_SEPARATOR = '-'
PLACE_HOLDER_4_MISSING_VALUE = '/'


class ReferenceMask(Template):
    pattern = r'''\[(?:
                    (?P<escaped>\[) |
                    (?P<named>[^\]]+?)\] |
                    (?P<braced>[^\]]+?)\] |
                    (?P<invalid>)
                    )'''


def extract_token(s):
    pattern = re.compile(r'\[([^\]]+?)\]')
    return set(pattern.findall(s))


def sanitize_reference_mask(product, mask):
    tokens = extract_token(mask)
    attribute_names = set()
    for line in product.attribute_line_ids:
        attribute_names.add(line.attribute_id.name)
    if not tokens.issubset(attribute_names):
        raise MissingError(_('Found unrecognized attribute name in '
                             '"Partcode Template"'))


def get_rendered_default_code(product, mask):
    product_attrs = defaultdict(str)
    reference_mask = ReferenceMask(mask)
    for value in product.attribute_value_ids:
        if value.attribute_code:
            product_attrs[value.attribute_id.name] += value.attribute_code
    all_attrs = extract_token(mask)
    missing_attrs = all_attrs - set(product_attrs.keys())
    missing = dict.fromkeys(missing_attrs, PLACE_HOLDER_4_MISSING_VALUE)
    product_attrs.update(missing)
    default_code = reference_mask.safe_substitute(product_attrs)
    return default_code


def render_default_code(product, mask):
    sanitize_reference_mask(product, mask)
    product.default_code = get_rendered_default_code(product, mask)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    reference_mask = fields.Char(
        string='Partcode Template',
        help='A template for building internal references of a '
             'variant generated from this template.\n'

             'Example:\n'
             'A product named ABC with 2 attributes: Size and Color:\n'

             'Product: ABC\n'
             'Color: Red(r), Yellow(y), Black(b)  #Red, Yellow, Black are '
             'the attribute value, `r`, `y`, `b` are the corresponding code\n'
             'Size: L (l), XL(x)\n'

             'When setting the partcode template to `[Color]-[Size]`, the '
             'default code on the variants will be something like `r-l` '
             '`b-l` `r-x` ...\n'

             'If you like, You can even have the attribute name appear more'
             ' than once in the template e.g. `fancyA/[Size]~[Color]~[Size]`'
             ' When saved, the default code on variants will be something like'
             ' `fancyA/l~r~l` (for variant with Color "Red" and Size "L") '
             '`fancyA/x~y~x` (for variant with Color "Yellow" and Size "XL")\n'

             'Note: make sure characters "[,]" do not appear in your '
             'attribute name')

    @api.model
    def create(self, vals):
        product = self.new(vals)
        if not vals.get('reference_mask') and product.attribute_line_ids:
            attribute_names = []
            for line in product.attribute_line_ids:
                attribute_names.append("[{}]".format(line.attribute_id.name))
            default_mask = DEFAULT_REFERENCE_SEPARATOR.join(attribute_names)
            vals['reference_mask'] = default_mask
        elif vals.get('reference_mask'):
            sanitize_reference_mask(product, vals['reference_mask'])
        return super(ProductTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        for tmpl in self:
            if tmpl.attribute_line_ids and not tmpl.reference_mask:
                attribute_names = []
                for line in tmpl.attribute_line_ids:
                    attribute_names.append("[{}]".format(
                        line.attribute_id.name))
                default_mask = DEFAULT_REFERENCE_SEPARATOR.join(
                    attribute_names)
                tmpl.reference_mask = default_mask
            if tmpl.reference_mask:
                product_obj = self.env['product.product']
                cond = [('product_tmpl_id', '=', tmpl.id),
                        ('manual_code', '=', False)]
                products = product_obj.search(cond)
                for product in products:
                    if tmpl.reference_mask:
                        render_default_code(product, tmpl.reference_mask)
        return result


class ProductProduct(models.Model):
    _inherit = 'product.product'

    manual_code = fields.Boolean(string='Manual code',
                                 default=False)

    @api.model
    def create(self, values):
        product = super(ProductProduct, self).create(values)
        if product.reference_mask:
            render_default_code(product, product.reference_mask)
        return product

    @api.onchange('default_code')
    def onchange_default_code(self):
        self.manual_code = bool(self.default_code)


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'
    _order = 'attribute_sequence, sequence'

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.attribute_code = self.name[0:2]

    attribute_code = fields.Char(
        string='Attribute Code', default=onchange_name)
    attribute_sequence = fields.Integer(related='attribute_id.sequence',
                                        store=True, readonly=True)

    @api.model
    def create(self, values):
        if 'attribute_code' not in values:
            values['attribute_code'] = values.get('name', '')[0:2]
        value = super(ProductAttributeValue, self).create(values)
        return value

    @api.multi
    def write(self, vals):
        result = super(ProductAttributeValue, self).write(vals)
        if 'attribute_code' in vals:
            attribute_line_obj = self.env['product.attribute.line']
            product_obj = self.env['product.product']
            for attr_value in self:
                cond = [('attribute_id', '=', attr_value.attribute_id.id)]
                attribute_lines = attribute_line_obj.search(cond)
                for line in attribute_lines:
                    cond = [('product_tmpl_id', '=', line.product_tmpl_id.id),
                            ('manual_code', '=', False)]
                    products = product_obj.search(cond)
                    for product in products:
                        if product.reference_mask:
                            render_default_code(product,
                                                product.reference_mask)
        return result
