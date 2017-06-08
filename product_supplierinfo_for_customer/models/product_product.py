# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _name_get(self, dict_data):
        name = dict_data.get('name', '')
        code = (
            self.env.context.get('display_default_code', True) and
            dict_data.get('default_code', False) or
            False
        )
        if code:
            name = '[%s] %s' % (code, name)
        return (dict_data['id'], name)

    @api.multi
    def name_get(self):
        ResPartner = self.env['res.partner']
        result = super(ProductProduct, self).name_get()

        partner_id = self.env.context.get('sale_partner_id', False)
        if partner_id:
            partner_ids = [
                partner_id,
                ResPartner.browse(partner_id).commercial_partner_id.id,
            ]
            last_result = result
            result = []
            for product in self:
                customers = ResPartner
                result_tuple = filter(lambda r: r[0] == product.id, last_result)
                if partner_ids:
                    customers = product.customer_ids.filtered(
                        lambda pr: pr.name.id in partner_ids)
                if not customers:
                    result += [result_tuple and result_tuple[0]]
                    continue
                name = result_tuple and result_tuple[0][1] or ""
                variant = ", ".join(product.attribute_value_ids.mapped("name"))
                for customer in customers:
                    customer_variant = (
                        customer.product_name and (
                            variant and "%s (%s)" % (customer.product_name, variant) or
                            customer.product_name
                        ) or False)
                    mydict = {
                        'id': product.id,
                        'name': customer_variant or name,
                        'default_code': customer.product_code or product.default_code,
                    }
                    result += [self._name_get(mydict)]
        return result
