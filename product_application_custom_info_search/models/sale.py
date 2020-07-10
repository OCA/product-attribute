# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    application_filter_value_ids = fields.Many2many(
        'custom.info.value',
        'sale_order_filter_value_rel',
        'sale_id',
        'value_id',
        string='Application Filter Values',
        copy=False,
        readonly=True)

    application_product_tmpl_ids = fields.Many2many(
        'product.template', compute='_compute_application_product_tmpl_ids'
    )

    filtered_applications = fields.Boolean(
        string='Application Filter', compute='_compute_filtered_applications')

    @api.multi
    def _compute_application_product_tmpl_ids(self):
        product_app_obj = self.env['product.application']

        for order in self:
            filtered_product_tmpl_ids = []
            if order.application_filter_value_ids:
                for value in order.application_filter_value_ids:
                    cur_product_tmpl_ids =\
                        product_app_obj.get_filtered_product_tmpl_ids(
                            value.property_id, value)
                    if filtered_product_tmpl_ids:
                        # intersection:
                        filtered_product_tmpl_ids = list(
                            set(filtered_product_tmpl_ids) &
                            set(cur_product_tmpl_ids))
                    else:
                        filtered_product_tmpl_ids = cur_product_tmpl_ids
#             else:
#                 filtered_product_tmpl_ids = product_tmpl_obj.search(
#                     [('sale_ok', '=', True)]).ids
            order.application_product_tmpl_ids = filtered_product_tmpl_ids

    @api.multi
    def _compute_filtered_applications(self):
        for order in self:
            filtered_applications = False
            if order.application_product_tmpl_ids:
                filtered_applications = True
            order.filtered_applications = filtered_applications

    @api.multi
    def open_filter_application_wizard(self):
        filter_app_obj = self.env['filter.application.wizard']

        self.ensure_one()

        wiz_lines_vals = []
        for value in self.application_filter_value_ids:
            wiz_line_vals = ({
                'property_id': value.property_id.id,
                'value': value.value_id.id
            })
            wiz_lines_vals.append((0, False, wiz_line_vals))
        wiz_vals = {
            'filter_line_ids': wiz_lines_vals,
        }

        wiz = filter_app_obj.create(wiz_vals)

        action = {
            'name': _('Select Products by Applications'),
            'type': 'ir.actions.act_window',
            'res_model': 'filter.application.wizard',
            'res_id': wiz.id,
            'target': 'new',
            'view_mode': 'form',
            'context': {'from_sale_order': True},
        }

        return action
