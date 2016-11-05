# -*- coding: utf-8 -*-
##############################################################################
#
#    Sale - Food Module for Odoo
#    Copyright (C) 2012-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
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

from openerp import api, fields, models, _


class ProductPricetagWizard(models.TransientModel):
    _name = 'product.pricetag.wizard'
    _rec_name = 'offset'

    # Fields Function Section
    @api.model
    def _domain_get(self):
        return [
            ('to_print', '=', True),
            ('category_print_id', '=', self.category_print_id.id)]

    @api.model
    def _get_default_print_category(self):
        active_id = self.env.context.get('active_id', False)
        if active_id:
            return self.env['product.category.print'].browse(active_id)
        else:
            pcp = self.env['product.category.print'].search([])
            return pcp and pcp[0] or False

    @api.model
    def _get_line_ids(self):
        res = []
        dom = self._domain_get()
        pp_obj = self.env['product.product']
        pp_ids = pp_obj.search(dom)
        for pp_id in pp_ids:
            res.append((0, 0, {
                'product_id': pp_id,
                'quantity': 1,
                'print_unit_price': True,
            }))
        return res

    @api.onchange('category_print_id')
    def _onchange_category_print_id(self):
        self.ensure_one()
        res = []
        dom = self._domain_get()
        pp_obj = self.env['product.product']
        pp_ids = pp_obj.search(dom)
        for pp_id in pp_ids:
            res.append((0, 0, {
                'product_id': pp_id,
                'quantity': 1,
                'print_unit_price': True,
            }))
        self.line_ids = res

    # Columns Section
    offset = fields.Integer(
        'Offset', required=True, help="Number of empty pricetags", default=0)
    category_print_id = fields.Many2one(
        'product.category.print', 'Print Category', required=True,
        default=lambda s: s._get_default_print_category())
    line_ids = fields.One2many(
        'product.pricetag.wizard.line', 'wizard_id', 'Products',
        default=lambda s: s._get_line_ids())
    # border = fields.Boolean('Add a border', default=False)

    @api.multi
    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self._get_data_form()
        action = self.category_print_id.pricetag_model_id.report_model

        # mark the selected products as Up To Date
        self.line_ids.mapped('product_id').write({'to_print': False})

        return self.env['report'].get_action(
            self, action, data=data)

    @api.multi
    def initialize_product(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Print Price Tags'),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'product.pricetag.wizard',
            'res_id': None,
            'target': 'new',
        }

    @api.model
    def _get_data_form(self):
        res = {}
        res['line_ids'] = [line.id for line in self.line_ids]
        res['fields'] = self._get_pricetag_fields()
        res['category_print_id'] = self.category_print_id.id
        # res['border'] = self.border
        return res

    @api.model
    def _get_pricetag_fields(self):
        return [f.id for f in self.category_print_id.field_ids]


class ProductPricetagWizardLine(models.TransientModel):
    _name = 'product.pricetag.wizard.line'
    _rec_name = 'product_id'

    # Columns Section
    wizard_id = fields.Many2one(
        'product.pricetag.wizard', 'Wizard', select=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    quantity = fields.Integer('Quantity', required=True, default=1)
