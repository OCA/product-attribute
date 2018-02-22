# Copyright (C) 2018 - TODAY, Open Source Integrators
# Integrators License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import api, fields as fields_cls, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    eol_date = fields_cls.Date(
        compute='_compute_eol_date',
        inverse='_inverse_eol_date',
        string='End of Life Date',
        index=True)

    @api.depends('product_variant_ids', 'product_variant_ids.eol_date')
    def _compute_eol_date(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.eol_date = template.product_variant_ids.eol_date

    @api.multi
    def _inverse_eol_date(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.eol_date = self.eol_date


class ProductVariants(models.Model):
    _inherit = 'product.product'

    eol_date = fields_cls.Date(
        string='End of Life Date',
        index=True)

    @api.model
    def _prepare_msg_values(self):
        mail_msg = self.env.ref('product_end_of_life.mail_message_product_eol')
        msg_values = {
            'res_id': mail_msg.res_id,
            'model': mail_msg.model,
            'subject': mail_msg.subject,
            'message_type': mail_msg.message_type,
            'subtype_id': mail_msg.subtype_id}
        return msg_values

    @api.model
    def send_eol_mail(self, product_list):
        msg_values = self._prepare_msg_values()
        self.message_post_with_view('product_end_of_life.message_product_eol',
                                    values={'self': self,
                                            'origin': product_list},
                                    **msg_values)

    @api.model
    def send_notify_product_eol(self):
        param_values = self.env['res.config.settings'].get_values()
        interval = param_values['product_eol_approaching_number']
        uot = param_values['product_eol_approaching_type']

        dt_interval = relativedelta(**{uot: interval})
        next_win_date_start = date.today() + dt_interval
        next_win_date_end = (next_win_date_start + dt_interval -
                             relativedelta(days=1))

        product_list = self.search([('eol_date', '>=', next_win_date_start),
                                    ('eol_date', '<=', next_win_date_end),
                                    ('type', '=', 'product')])
        if product_list:
            self.send_eol_mail(product_list)

        cron = self.env.ref('product_end_of_life.ir_cron_notify_product_eol')
        cron.write({'interval_number': interval,
                    'interval_type': uot,
                    'nextcall': datetime.combine(next_win_date_start,
                                                 datetime.min.time())})
        return True

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self.env.context.get('source_from') == 'purchase_order':
            today = fields_cls.Date.today()
            args = (args or []) + ['|', ['eol_date', '>', today],
                                   ['eol_date', '=', False]]
        return super(ProductVariants, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None,
                    order=None):
        if self.env.context.get('source_from') == 'purchase_order':
            today = fields_cls.Date.today()
            domain = (domain or []) + ['|', ['eol_date', '>', today],
                                       ['eol_date', '=', False]]
        return super(ProductVariants, self).search_read(
            domain=domain, fields=fields, offset=offset,
            limit=limit, order=order
        )
