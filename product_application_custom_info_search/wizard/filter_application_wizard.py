# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class FilterApplicationWizard(models.TransientModel):
    _name = 'filter.application.wizard'
    _description = 'Search products by Application attributes'

    filter_line_ids = fields.One2many(
        'filter.application.line.wizard',
        'filter_wizard_id',
        string='Filter Lines'
    )

    @api.multi
    def apply_filters(self):
        self.ensure_one()

        product_tmpl_ids = []

        for filter in self.filter_line_ids:
            pass

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

    @api.onchange('property_id')
    def onchange_property_id(self):
        domain = {}
        filtered_product_tmpl_ids = []
        already_filtered_properties = []
        for previous_line in self.filter_wizard_id.filter_line_ids:
            if previous_line.property_id and previous_line.value_id:
                already_filtered_properties.append(previous_line.property_id.id)
            if previous_line.id == self.id:
                continue
            # Get all product applications according previous selection:
            product_app_model = self.env.ref(
                'product_application.model_product_application')
            field_type = previous_line.property_id.field_type
            if field_type == 'bool':
                value_bool = 'f'
                if previous_line.value_id.value_bool:
                    value_bool = 't'
                where_value = 'AND prop.field_type = \'bool\' AND val.value_bool = \'%s\'' % value_bool
            elif field_type == 'float':
                where_value = 'AND prop.field_type = \'float\' AND val.value_float = %s' % previous_line.value_id.value_float
            elif field_type == 'str':
                where_value = 'AND prop.field_type = \'str\' AND val.value_str = \'%s\'' % previous_line.value_id.value_str
            elif field_type == 'int':
                where_value = 'AND prop.field_type = \'int\' AND val.value_int = %s' % previous_line.value_id.value_int
            elif field_type == 'id':
                where_value = 'AND prop.field_type = \'id\' AND val.value_id = %s' % previous_line.value_id.value_id.id
            else:
                raise

            query = '''SELECT
    prod_app.product_tmpl_id
FROM
    custom_info_property prop,
    custom_info_template tmpl,
    custom_info_value val,
    product_application prod_app
WHERE
    tmpl.model_id = %s
    AND prop.template_id = tmpl.id
    AND val.property_id = prop.id
    AND prod_app.custom_info_template_id = tmpl.id
    AND prod_app.id = val.res_id
    AND prop.id = %s
    
'''
            query += where_value
            self.env.cr.execute(
                query, tuple([product_app_model.id, previous_line.property_id.id])
            )
            cur_product_tmpl_ids = [row[0] for row in self.env.cr.fetchall()]
            if filtered_product_tmpl_ids:
                filtered_product_tmpl_ids = list(set(filtered_product_tmpl_ids)&set(cur_product_tmpl_ids))
            else:
                filtered_product_tmpl_ids = cur_product_tmpl_ids

        if filtered_product_tmpl_ids:
            # get availablel properties:
            query = '''SELECT
    prop.id
FROM
    product_application prod_app,
    custom_info_property prop
WHERE
    prod_app.product_tmpl_id IN (%s)
    AND prod_app.custom_info_template_id = prop.template_id;
'''
            self.env.cr.execute(
                query,
                (filtered_product_tmpl_ids)
            )
            available_properties = [row[0] for row in self.env.cr.fetchall()]
            final_available_properties = []
            for cur_prop in available_properties:
                if cur_prop not in already_filtered_properties:
                    final_available_properties.append(cur_prop)
            domain.update({'property_id': [('id', 'in', final_available_properties)]})

        if self.property_id:
            domain.update({'value_id': [('property_id', '=', self.property_id.id)]})
        result = {'domain': domain}

        return result
