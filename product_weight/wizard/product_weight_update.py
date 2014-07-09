# -*- coding: utf-8 -*-

##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
#    Copyright (C) 2015 Akretion (<http://www.akretion.com>).
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProductWeightUpdate(models.TransientModel):
    _name = "product.weight.update"
    _description = "Update Product Weight"

    product_tmpl_id = fields.Many2one('product.template', 'Product')
    bom_id = fields.Many2one(
        'mrp.bom',
        'BoM',
        domain="[('product_tmpl_id', '=', product_tmpl_id)]")

    @api.model
    def default_get(self, fields):
        res = super(ProductWeightUpdate, self).default_get(fields)
        if not fields:
            return res
        context = self.env.context
        if context.get('active_model') == 'product.template':
            product_tmpl_id = context.get('active_id', False)
            domain_template = [('product_tmpl_id', '=', product_tmpl_id)]
            domain_product = []
        else:
            product_id = context.get('active_id', False)
            product = self.env['product.product'].browse(product_id)
            product_tmpl_id = product.product_tmpl_id.id
            domain_template = [('product_tmpl_id', '=', product_tmpl_id)]
            domain_product = [('product_id', '=', product_id)]
        bom = False
        if domain_product:
            bom = self.env['mrp.bom'].search(domain_product, limit=1)
        if not domain_product or not bom:
            bom = self.env['mrp.bom'].search(domain_template, limit=1)
        if bom:
            res.update({'bom_id': bom.id})

        if 'product_tmpl_id' in fields:
            res.update({'product_tmpl_id': product_tmpl_id})
        return res

    @api.multi
    def calculate_product_bom_weight(self, bom):
        uom_obj = self.env['product.uom']
        product_tmpl = bom.product_tmpl_id
        tmpl_qty = uom_obj._compute_qty(
            bom.product_uom.id,
            bom.product_qty,
            product_tmpl.uom_id.id)
        bom_lines = bom.bom_line_ids.get_final_components()
        weight_gross = 0.0
        weight_net = 0.0
        for line in bom_lines:
            component_tmpl = line.product_id.product_tmpl_id
            component_qty = uom_obj._compute_qty(
                line.product_uom.id,
                line.product_qty,
                component_tmpl.uom_id.id)
            weight_net += component_tmpl.weight_net * component_qty
            weight_gross += component_tmpl.weight * component_qty
            _logger.info("%s : %0.2f | %0.2f",
                         bom.product_tmpl_id.name,
                         weight_net, weight_gross)
        weight_net = weight_net / tmpl_qty
        weight_gross = weight_gross / tmpl_qty
        product_tmpl.write({'weight': weight_gross, 'weight_net': weight_net})

    @api.multi
    def update_single_weight(self):
        self.ensure_one()
        self.calculate_product_bom_weight(self.bom_id)
        return {}

    @api.multi
    def update_multi_product_weight(self):
        self.ensure_one()
        product_obj = self.env['product.product']
        context = self.env.context
        if context.get('active_model') == 'product.template':
            template_ids = context.get('active_ids', [])
        else:
            product_ids = context.get('active_ids', [])
            products = product_obj.browse(product_ids)
            template_ids = products.mapped('product_tmpl_id').ids
        for template_id in template_ids:
            bom = self.env['mrp.bom'].search(
                [('product_tmpl_id', '=', template_id)], limit=1)
            if bom:
                self.calculate_product_bom_weight(bom)
