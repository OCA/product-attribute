# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class FilterApplicationWizard(models.TransientModel):
    _name = 'filter.application.wizard'
    _description = 'Search products by Application attributes'

    filter_line_ids = fields.One2many(
        'filter.application.line.wizard',
        'filter_wizard_id',
        string='Filter Lines'
    )

    product_tmpl_ids = fields.Many2many(
        comodel_name='product.template', string='Products Template',)

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template', string='Product Template')

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product')

    order_id = fields.Many2one(
        comodel_name='sale.order', string='Sale Order')

    @api.onchange('product_tmpl_id')
    def onchange_product_tmpl_id(self):
        product_obj = self.env['product.product']

        self.product_id = False
        if self.product_tmpl_id:
            products = product_obj.search([
                ('product_tmpl_id', '=', self.product_tmpl_id.id)
            ])
            if products:
                self.product_id = products[0]

    @api.multi
    def apply_filters(self):
        self.ensure_one()

        product_tmpl_ids = self.filter_line_ids.apply_filters()

        if self._context.get('from_sale_order', False):
            # Called from sale order form:
            if self.env.context['active_id']\
                    and self.env.context['active_model'] == 'sale.order':
                self.order_id = self.env.context['active_id']
            self.order_id.write({
                'application_filter_value_ids':
                    [(6, False, self.filter_line_ids.get_values().ids)],
            })
            self.product_tmpl_ids = product_tmpl_ids
            if product_tmpl_ids:
                self.product_tmpl_id = product_tmpl_ids[0]
                self.onchange_product_tmpl_id()

            action = True
        else:
            # Called from products:
            action = {
                'name': _('Products'),
                'type': 'ir.actions.act_window',
                'res_model': 'product.template',
                'target': 'current',
            }

            if len(product_tmpl_ids) == 1:
                action['res_id'] = product_tmpl_ids[0]
                action['view_mode'] = 'form'
            else:
                action['view_mode'] = 'tree,form'
                action['domain'] = [('id', 'in', product_tmpl_ids)]

        return action

    @api.multi
    def add_products(self):
        self.ensure_one()

        self.order_id.write({
            'order_line': [(0, False, {'product_id': self.product_id.id})]}
        )

        return True

    @api.model
    def create(self, vals):
        res = super(FilterApplicationWizard, self).create(vals)
        return res


class FilterApplicationLineWizard(models.TransientModel):
    _name = 'filter.application.line.wizard'

    filter_wizard_id = fields.Many2one(
        'filter.application.wizard',
        string='Filter Application Wizard',
    )

    property_id = fields.Many2one(
        'custom.info.property',
        string='Custom Property',
        domain=[('template_id.model', '=', 'product.application')]
    )

    value_id = fields.Many2one(
        'custom.info.value',
        string='Custom Value',
    )

    @api.multi
    def apply_filters(self, skip_line_id=False):
        product_app_obj = self.env['product.application']

        filtered_product_tmpl_ids = []
        for line in self:
            if skip_line_id == line.id:
                continue
            if line.property_id and line.value_id:
                cur_product_tmpl_ids =\
                    product_app_obj.get_filtered_product_tmpl_ids(
                        line.property_id, line.value_id)
                if filtered_product_tmpl_ids:
                    # intersection:
                    filtered_product_tmpl_ids = list(
                        set(filtered_product_tmpl_ids) &
                        set(cur_product_tmpl_ids))
                else:
                    filtered_product_tmpl_ids = cur_product_tmpl_ids
        return filtered_product_tmpl_ids

    @api.onchange('property_id')
    def onchange_property_id(self):
        domain = {}
        already_filtered_properties = []
        for previous_line in self.filter_wizard_id.filter_line_ids:
            already_filtered_properties.append(previous_line.property_id.id)
        filtered_product_tmpl_ids =\
            self.filter_wizard_id.filter_line_ids.apply_filters(
                skip_line_id=self.id)

        if filtered_product_tmpl_ids:
            # get available properties:
            query = '''SELECT
    DISTINCT prop.id
FROM
    product_application prod_app,
    custom_info_property prop
WHERE
    prod_app.product_tmpl_id IN %s
    AND prod_app.custom_info_template_id = prop.template_id;
'''
            self.env.cr.execute(
                query,
                [tuple(filtered_product_tmpl_ids)]
            )
            available_properties = [row[0] for row in self.env.cr.fetchall()]
            final_available_properties = []
            for cur_prop in available_properties:
                if cur_prop not in already_filtered_properties:
                    final_available_properties.append(cur_prop)
            domain.update(
                {'property_id': [('id', 'in', final_available_properties)]})

        if self.property_id:
            if filtered_product_tmpl_ids:
                query = '''SELECT
    MAX(val.id)
FROM
    custom_info_value val,
    custom_info_property prop,
    custom_info_template tmpl,
    product_application prod_app
WHERE
    prop.id = %s
    AND prop.id = val.property_id
    AND prop.template_id = tmpl.id
    AND tmpl.id = prod_app.custom_info_template_id
    AND prod_app.product_tmpl_id IN %s
    AND val.res_id = prod_app.id
    AND val.model = 'product.application'
GROUP BY (val.value_str, val.value_int, val.value_float, val.value_bool,
    val.value_id)
'''
                self.env.cr.execute(
                    query,
                    tuple([
                        self.property_id.id,
                        tuple(filtered_product_tmpl_ids)
                    ])
                )
            else:
                query = '''SELECT
    MAX(val.id)
FROM
    custom_info_value val,
    custom_info_property prop
WHERE
    prop.id = %s
    AND prop.id = val.property_id
GROUP BY (val.value_str, val.value_int, val.value_float, val.value_bool,
    val.value_id)
'''
                self.env.cr.execute(
                    query,
                    tuple([self.property_id.id])
                )
            available_value_ids = [row[0] for row in self.env.cr.fetchall()]
            domain.update({'value_id': [('id', 'in', available_value_ids)]})
        result = {'domain': domain}

        return result

    @api.multi
    def get_values(self):
        values = self.env['custom.info.value']
        for line in self:
            values |= line.value_id

        return values
