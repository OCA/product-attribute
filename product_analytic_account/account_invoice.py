# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product Analytic Account module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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

from openerp import models, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def product_id_change(
            self, product, uom_id, qty=0, name='', type='out_invoice',
            partner_id=False, fposition_id=False, price_unit=False,
            currency_id=False, company_id=None):
        res = super(AccountInvoiceLine, self).product_id_change(
            product, uom_id, qty=qty, name=name, type=type,
            partner_id=partner_id, fposition_id=fposition_id,
            price_unit=price_unit,
            currency_id=currency_id, company_id=company_id)
        if company_id is not None:
            company_id = company_id
        else:
            company_id = self._context.get('company_id', False)
        self = self.with_context(
            company_id=company_id, force_company=company_id)
        if product:
            product_o = self.env['product.product'].browse(product)
            account_analytic_id = False
            if type in ('out_invoice', 'out_refund'):
                account_analytic_id =\
                    product_o.income_analytic_account_id.id or\
                    product_o.categ_id.income_analytic_account_id.id
            else:
                account_analytic_id =\
                    product_o.expense_analytic_account_id.id or\
                    product_o.categ_id.expense_analytic_account_id.id
            if account_analytic_id:
                res['value']['account_analytic_id'] = account_analytic_id
        return res
