
# -*- encoding: utf-8 -*-
##############################################################################
#
#    Daniel Campos (danielcampos@avanzosc.es) Date: 15/09/2014
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, exceptions, api, _


class ProductPricelistLoad(models.Model):
    _name = 'product.pricelist.load'
    _description = 'Product Price List Load'

    name = fields.Char('Load')
    date = fields.Date('Date:', readonly=True)
    file_name = fields.Char('File Name', readonly=True)
    file_lines = fields.One2many('product.pricelist.load.line', 'file_load',
                                 'Product Price List Lines')
    fails = fields.Integer('Fail Lines:', readonly=True)
    process = fields.Integer('Lines to Process:', readonly=True)
    supplier = fields.Many2one('res.partner')

    @api.multi
    def process_lines(self):
        for file_load in self:
            if not file_load.supplier:
                raise exceptions.Warning(_("You must select a Supplier"))
            product_obj = self.env['product.product']
            psupplinfo_obj = self.env['product.supplierinfo']
            pricepinfo_obj = self.env['pricelist.partnerinfo']
            if not file_load.file_lines:
                raise exceptions.Warning(_("There must be one line at least to"
                                           " process"))
            for line in file_load.file_lines:
                # process fail lines
                if line.fail:
                    # search product code
                    if line.code:
                        product_lst = product_obj.search([('default_code', '=',
                                                           line.code)])
                        if product_lst:
                            psupplinfo = psupplinfo_obj.create(
                                {'name': file_load.supplier.id,
                                 'product_tmpl_id':
                                 product_lst[0].product_tmpl_id.id})
                            pricepinfo_obj.create(
                                {'suppinfo_id': psupplinfo.id,
                                 'min_quantity': psupplinfo.min_qty,
                                 'price': line.price})
                            file_load.fails -= 1
                            line.write(
                                {'fail': False,
                                 'fail_reason': _('Correctly Processed')})
                        else:
                            line.fail_reason = _('Product not found')
        return True


class ProductPricelistLoadLine(models.Model):
    _name = 'product.pricelist.load.line'
    _description = 'Product Price List Load Line'

    code = fields.Char('Product Code', required=True)
    info = fields.Char('Product Description')
    price = fields.Float('Product Price', required=True)
    discount_1 = fields.Float('Product Discount 1')
    discount_2 = fields.Float('Product Discount 2')
    retail = fields.Float('Retail Price', required=True)
    pdv1 = fields.Float('PDV1')
    pdv2 = fields.Float('PDV2')
    fail = fields.Boolean('Fail')
    fail_reason = fields.Char('Fail Reason')
    file_load = fields.Many2one('product.pricelist.load', 'Load',
                                required=True)
