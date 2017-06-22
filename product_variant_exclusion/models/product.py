# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, UserError
import psycopg2


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    variant_exclusion_ids = fields.One2many(
        'product.variant.exclusion', 'product_tmpl_id', 'Variants exclusion'
    )

    allowed_value_ids = fields.Many2many('product.attribute.value',
                                         compute='_compute_allowed_values')

    @api.depends('attribute_line_ids.value_ids')
    def _compute_allowed_values(self):
        for template in self:
            template.allowed_value_ids = template.attribute_line_ids.mapped(
                'value_ids')

    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if 'variant_exclusion_ids' in vals:
            self.create_variant_ids()
            self.delete_variant_ids()
        return res

    @api.multi
    def delete_variant_ids(self):
        exclusions = self.env['product.variant.exclusion'].search(
            [('product_tmpl_id', '=', self.id)])
        for template in self:
            for product in template.product_variant_ids:
                for excl in exclusions:
                    if set(excl.attribute_value_ids.ids) <= set(
                            product.attribute_value_ids.ids):
                        try:
                            with self.env.cr.savepoint():
                                product.unlink()
                        except (psycopg2.Error, ValidationError):
                            product.write({'active': False})
                        break


class ProductAttributeLine(models.Model):

    _inherit = 'product.attribute.line'

    @api.multi
    def write(self, vals):
        attr_values = vals.get('value_ids', False) and vals.get(
            'value_ids')[0][2]
        if attr_values and len(attr_values) <= 1:
            for line in self:
                for exclusion in line.product_tmpl_id.variant_exclusion_ids:
                    if set(attr_values) <= set(
                            exclusion.attribute_value_ids.ids):
                        raise UserError(_(
                            'You cannot leave only one attribute value on a '
                            'line if this value is part of an exclusion'))
        if self.value_ids.ids != attr_values:
            new_values = self.env[
                'product.attribute.value'].browse(attr_values)
            exclusion_values = self.product_tmpl_id.variant_exclusion_ids\
                .mapped('attribute_value_ids')
            for new_val in new_values:
                if new_val in exclusion_values:
                    raise UserError(_('You cannot remove an attribute value '
                                      'from an attribute line, if this value '
                                      'is part of an exclusion.'))
        return super(ProductAttributeLine, self).write(vals)

    @api.multi
    def unlink(self):
        for line in self:
            for val_id in line.value_ids.ids:
                if val_id in line.product_tmpl_id.variant_exclusion_ids.mapped(
                        'attribute_value_ids').ids:
                    raise UserError(_(
                        'You cannot delete an attribute line when '
                        'one of its values is part of an exclusion'))
        return super(ProductAttributeLine, self).unlink()


class ProductVariantExclusion(models.Model):

    _name = 'product.variant.exclusion'

    product_tmpl_id = fields.Many2one('product.template', required=True)
    attribute_value_ids = fields.Many2many('product.attribute.value',
                                           required=True)

    def _check_values_attributes_uniqueness(self, value_ids):
        values = self.env['product.attribute.value'].browse(value_ids)
        attributes = values.mapped('attribute_id')
        if len(values) != len(attributes):
            raise UserError(_('You cannot have multiple values from the '
                              'same attribute in an exclusion.'))

    @api.model
    def create(self, vals):
        value_ids = vals.get('attribute_value_ids')[0][2]
        if len(value_ids) <= 1:
            raise UserError(_(
                'You cannot create an exclusion with only one value !'))
        template_lines = self.env['product.attribute.line'].search([
            ('product_tmpl_id', '=', vals.get('product_tmpl_id')),
            ('value_ids', 'in', value_ids)])
        for line in template_lines:
            if len(line.value_ids) <= 1 or set(line.value_ids.ids) <= set(
                    value_ids):
                raise UserError(_(
                    'You cannot create an exclusion for an attribute value '
                    'which is unique in its attribute line !'))
        self._check_values_attributes_uniqueness(value_ids)
        return super(ProductVariantExclusion, self).create(vals)

    @api.multi
    def write(self, vals):
        value_ids = vals.get('attribute_value_ids')[0][2]
        if len(value_ids) <= 1:
            raise UserError(_(
                'You cannot modify an exclusion to have only one value !'))
        self._check_values_attributes_uniqueness(value_ids)
        return super(ProductVariantExclusion, self).write(vals)


class ProductProduct(models.Model):

    _inherit = 'product.product'

    @api.multi
    def write(self, vals):
        if self._context.get('create_product_variant'):
            products_to_write = self.env['product.product']
            # Case 2: Setting active to True
            if vals.get('active', False):
                for product in self:
                    product_value_ids = product.attribute_value_ids.ids
                    if product.product_tmpl_id.variant_exclusion_ids:
                        for excl in product.product_tmpl_id.\
                                variant_exclusion_ids:
                            if not set(excl.attribute_value_ids.ids) <= set(
                                    product_value_ids):
                                products_to_write += product
                    else:
                        products_to_write += product
                return super(ProductProduct, products_to_write).write(vals)
        # Case 1: Adding new attribute value
        # Case 3: Setting active to False
        # Any other case
        return super(ProductProduct, self).write(vals)

    @api.model
    def create(self, vals):
        # Case 4: Creating new product variant
        if self._context.get('create_product_variant'):
            template_id = vals.get('product_tmpl_id')
            value_ids = vals.get('attribute_value_ids')[0][2]

            template_exclusions = self.env['product.variant.exclusion'].search(
                [('product_tmpl_id', '=', template_id)])

            for excl in template_exclusions:
                if set(excl.attribute_value_ids.ids) <= set(value_ids):
                    return self

        return super(ProductProduct, self).create(vals)
