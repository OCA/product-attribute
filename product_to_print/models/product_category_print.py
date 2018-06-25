# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api, _


class ProductCategoryprint(models.Model):
    _name = 'product.category.print'
    _inherit = 'ir.needaction_mixin'

    # View Section
    @api.model
    def _needaction_count(self, domain=None, context=None):
        product_obj = self.env['product.product']
        return len(product_obj.search([('to_print', '=', True)]))

    @api.model
    def _get_default_model(self):
        return self.env['pricetag.model'].search([], limit=1)

    # Fields Section
    name = fields.Char(string='Name', required=True)

    company_id = fields.Many2one(
        string='Company', comodel_name='res.company', index=True,
        default=lambda self: self.env['res.company']._company_default_get())

    product_ids = fields.One2many(
        comodel_name='product.product', inverse_name='category_print_id',
        string='Products')

    product_qty = fields.Integer(
        string='Products Quantity', compute='_compute_product_qty',
        store=True)

    product_to_print_ids = fields.One2many(
        comodel_name='product.product', compute='_compute_to_print',
        multi='to_print', string='Products To Print')

    product_to_print_qty = fields.Integer(
        compute='_compute_to_print',
        multi='to_print', string='Products Quantity To Print')

    product_to_print_rate = fields.Float(
        compute='_compute_to_print',
        multi='to_print', string='Products Quantity To Print (%)')

    field_ids = fields.Many2many(
        comodel_name='ir.model.fields',
        relation='product_category_print_field_rel', column1='category_id',
        column2='field_id', domain="[('model', '=', 'product.template')]")

    pricetag_model_id = fields.Many2one(
        'pricetag.model', 'Pricetag Model',
        default=lambda s: s._get_default_model())

    # Compute Section
    @api.multi
    @api.depends('product_ids.category_print_id')
    def _compute_product_qty(self):
        for category in self:
            category.product_qty = len(category.product_ids)

    @api.multi
    def _compute_to_print(self):
        product_obj = self.env['product.product']
        for category in self:
            products = product_obj.search([
                ('category_print_id', '=', category.id),
                ('to_print', '=', True)])
            category.product_to_print_qty = len(products)
            category.product_to_print_ids = products
            if category.product_qty:
                category.product_to_print_rate =\
                    float(len(products)) / category.product_qty
            else:
                category.product_to_print_rate = 0

    # View Section
    @api.multi
    def products_to_print(self):
        ctx = self._context.copy()
        ctx.update({
            'journal_category_print_id': self.id,
            'default_category_print_id': self.id})
        return {
            'name': _('Products To Print'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'product.product',
            'context': ctx,
        }
