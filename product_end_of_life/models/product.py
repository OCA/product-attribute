# Copyright (C) 2018 - TODAY, Open Source Integrators
# Integrators License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import api, fields as fields_cls, models, _
from odoo.osv import expression


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


class ProductProduct(models.Model):
    _inherit = 'product.product'

    eol_date = fields_cls.Date(
        string='End of Life Date',
        index=True)

    @api.model
    def _prepare_msg_values(self):
        msg_values = {
            'res_id': self.env.ref(
                'product_end_of_life.channel_product_eol').id,
            'model': 'mail.channel',
            'subject': _('Product End-Of-Life Notification'),
            'message_type': 'comment',
            'subtype_id': self.env.ref('mail.mt_comment').id}
        return msg_values

    @api.model
    def send_eol_mail(self, product_list):
        msg_values = self._prepare_msg_values()
        product_list[0].message_post_with_view(
            'product_end_of_life.message_product_eol',
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
        args = args or []
        domain = []
        if name:
            domain = [
                ('name', operator, name)
            ]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        products = self.search(domain + args, limit=limit)
        return products.name_get()

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self.env.context.get('source_from') == 'purchase_order':
            today = date.today()
            args = (args or []) + ['|', ['eol_date', '>', today],
                                   ['eol_date', '=', False]]
        return super(ProductProduct, self).search(args, offset=offset,
                                                  limit=limit, order=order,
                                                  count=count)
