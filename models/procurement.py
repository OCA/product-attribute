# -*- coding: utf-8 -*-
# © 2015 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProcurementOrder(models.Model):
    _inherit='procurement.order'

    #Do not call super as we do not want the native behaviour
    @api.model
    def _get_product_supplier(self, procurement):
        '''returns the main supplier of the procurement's product
           given as argument'''
        product = procurement.product_id
        company_supplier = self.env['product.supplierinfo'].search([
            '|',
            '&',
            ('product_tmpl_id', '=', product.product_tmpl_id.id),
            ('product_id', '=', False),
            ('product_id', '=', product.id),
            ('company_id', '=', procurement.company_id.id),
            ], limit=1)
        if company_supplier:
            return company_supplier.name
        return procurement.product_id.seller_id
