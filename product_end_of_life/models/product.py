# Copyright (C) 2018 - TODAY, Open Source Integrators
# Integrators License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    eol_date = fields.Date(
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

    @api.model
    def _prepare_product_eol_list(self):
        mail_msg = self.env['mail.message'].browse(
            self.env.ref('product_end_of_life.mail_message_product_eol').id)
        msg_values = {
            'res_id': mail_msg.res_id,
            'model': mail_msg.model,
            'subject': mail_msg.subject,
            'message_type': mail_msg.message_type,
            'subtype_id': mail_msg.subtype_id}
        return msg_values

    @api.model
    def email_product_eol_list(self, product_eol_ids):
        if not product_eol_ids:
            return
        msg_values = self._prepare_product_eol_list()
        product_eol_ids[0].message_post_with_view(
            'product_end_of_life.message_product_eol',
            values={'self': product_eol_ids[0], 'origin': product_eol_ids},
            **msg_values)

    @api.model
    def send_notify_product_eol(self):
        # get the cronjob record
        ir_cron = self.env['ir.cron'].browse(
            self.env.ref('product_end_of_life.ir_cron_notify_product_eol').id)
        # set approaching eol interval
        if ir_cron.approaching_type == 'weeks':
            apr_day = ir_cron.approaching_number * 7
            apr_month = 0
        elif ir_cron.approaching_type == 'months':
            apr_day = 0
            apr_month = ir_cron.approaching_number
        else:
            apr_day = ir_cron.approaching_number
            apr_month = 0
        # set execute every interval
        if ir_cron.interval_type == 'weeks':
            int_day = ir_cron.interval_number * 7
            int_month = 0
        elif ir_cron.interval_type == 'months':
            int_day = 0
            int_month = ir_cron.interval_number
        elif ir_cron.interval_type == 'days':
            int_day = ir_cron.interval_number
            int_month = 0
        # does not support  minutes/hours interval type
        # use 1 day as a default value
        else:
            int_day = 1
            int_month = 0
            # force to reset value to 1 day for "Execution Every" field
            ir_cron.approaching_number = 1
            ir_cron.interval_type = 'days'
        run_day = fields.Datetime.from_string(ir_cron.nextcall).date()
        # Start Date is equal to  run_day + approaching interval
        if apr_day:
            start_date = run_day + timedelta(apr_day)
        else:
            start_date = run_day + relativedelta(months=apr_month)
        # End Date is equal to  run_day + approaching interval +
        # execution interval
        if int_day:
            end_date = start_date + timedelta(int_day)
        else:
            end_date = start_date + relativedelta(months=int_month)
        # search products that are days approaching Eol
        product_eol_ids = self.env['product.product'].search([
            ('eol_date', '>=', start_date),
            ('eol_date', '<=', end_date),
            ('type', '=', 'product')],
            order='eol_date')
        # send email to recipients from the Product Eol Discussion Channel.
        self.email_product_eol_list(product_eol_ids)
        return True


class ProductVariants(models.Model):
    _inherit = 'product.product'

    eol_date = fields.Date(
        string='End of Life Date',
        index=True)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        context = self._context
        if context.get('source_from') == 'purchase_order':
            today = fields.Date.today()
            if args:
                args += ['|', ['eol_date', '>', today],
                         ['eol_date', '=', False]]
            else:
                args = ['|', ['eol_date', '>', today],
                        ['eol_date', '=', False]]
        result = super(ProductVariants, self).name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit)
        return result

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None,
                    order=None):
        context = self._context
        if context.get('source_from') == 'purchase_order':
            today = str(datetime.today().date())
            if domain:
                domain += ['|', ['eol_date', '>', today],
                           ['eol_date', '=', False]]
            else:
                domain = ['|', ['eol_date', '>', today],
                          ['eol_date', '=', False]]
        res = super(ProductVariants, self).search_read(domain=domain,
                                                       fields=fields,
                                                       offset=offset,
                                                       limit=limit,
                                                       order=order)
        return res
