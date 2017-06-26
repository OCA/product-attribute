# coding: utf-8
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, models


class ProductProduct(models.Model):

    _inherit = "product.product"

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=80):
        res = super(ProductProduct, self).name_search(
            name, args=args, operator=operator, limit=limit)
        if res or not self._context.get('partner_id'):
            return res
        partner_id = self._context['partner_id']
        supplierinfo = self.env['product.supplierinfo'].search(
            [('name', '=', partner_id), '|', ('product_code', operator, name),
             ('product_name', operator, name)])
        product = self.search(
            [('product_tmpl_id', '=', supplierinfo.product_tmpl_id.id)],
            limit=limit)
        res = product.name_get()
        return res
