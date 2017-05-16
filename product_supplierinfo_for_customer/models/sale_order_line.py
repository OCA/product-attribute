# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def product_id_change(
            self, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False):

        ProductProduct = self.env["product.product"]
        product_id = product

        res = super(SaleOrderLine, self).product_id_change(
            pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,
            name=name, partner_id=partner_id, lang=lang, update_tax=update_tax,
            date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag)

        res.setdefault("value", {})
        if "name" in res["value"]:
            del res["value"]["name"]

        if product_id:
            if partner_id:
                ProductProduct = ProductProduct.with_context(sale_partner_id=partner_id)
            product = ProductProduct.browse(product_id)
            # Call name_get() with partner in the context to eventually match
            # name and description in the seller_ids field
            if not name:
                dummy, name = product.name_get()[0]
                if product.description_sale:
                    name += '\n' + product.description_sale
                res['value'].update({'name': name})
        return res
