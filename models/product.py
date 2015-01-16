# -*- encoding: utf-8 -*-
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
from openerp import models, fields, api, _
from openerp.exceptions import except_orm
import re
from string import Template
from collections import defaultdict

DEFAULT_REFERENCE_SEPERATOR = '-'
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
        raise except_orm(_('Error'), _('Found unrecognized attribute name in '
                                       '"Variant Reference Mask"'))


def render_default_code(product, mask):
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
    product.default_code = default_code


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    reference_mask = fields.Char(
        string='Variant reference mask',
        help='Reference mask for building internal references of a '
             'variant generated from this template.\n'

             'Example:\n'
             'A product named ABC with 2 attributes: Size and Color:\n'

             'Product: ABC\n'
             'Color: Red(r), Yellow(y), Black(b)  #Red, Yellow, Black are '
             'the attribute value, `r`, `y`, `b` are the corresponding code\n'
             'Size: L (l), XL(x)\n'

             'When setting Variant reference mask to `[Color]-[Size]`, the '
             'default code on the variants will be something like `r-l` '
             '`b-l` `r-x` ...\n'

             'If you like, You can even have the attribute name appear more'
             ' than once in the mask. Such as , `fancyA/[Size]~[Color]~[Size]`'
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
            default_mask = DEFAULT_REFERENCE_SEPERATOR.join(attribute_names)
            vals['reference_mask'] = default_mask
        elif vals.get('reference_mask'):
            sanitize_reference_mask(product, vals['reference_mask'])
        return super(ProductTemplate, self).create(vals)

    @api.one
    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        if vals.get('reference_mask'):
            sanitize_reference_mask(self, vals['reference_mask'])
            product_obj = self.env['product.product']
            cond = [('product_tmpl_id', '=', self.id)]
            products = product_obj.search(cond)
            for product in products:
                render_default_code(product, vals['reference_mask'])
        return result


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.one
    @api.depends('product_tmpl_id.reference_mask', 'attribute_value_ids',
                 'attribute_value_ids.attribute_code')
    def _compute_default_code(self):
        self.reference_mask = self.product_tmpl_id.reference_mask
        if self.reference_mask:
            render_default_code(self, self.reference_mask)
        else:
            attribute_names = []
            for line in self.attribute_line_ids:
                attribute_names.append("[{}]".format(line.attribute_id.name))
            self.default_code = DEFAULT_REFERENCE_SEPERATOR.join(
                attribute_names)

    default_code = fields.Char(string='Internal Reference', store=True,
                               compute='_compute_default_code')


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    _sql_constraints = [
        ('number_uniq', 'unique(name)', _('Attribute Name must be unique!'))]


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.attribute_code = self.name[0:2]

    attribute_code = fields.Char(
        string='Attribute Code', default=onchange_name)

    @api.model
    def create(self, values):
        if 'attribute_code' not in values:
            values['attribute_code'] = values.get('name', '')[0:2]
        value = super(ProductAttributeValue, self).create(values)
        return value
