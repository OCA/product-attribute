# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class product_pricelist(models.Model):
    _inherit = 'product.pricelist'

    show_on_products = fields.Boolean(string="Display on product page")
    product_price = fields.Float(
            compute="get_custom_product_price",
            inverse="_set_custom_product_price",
            string="Price"
    )
    product_id = fields.Integer(
            #comodel_name="product.product",
            compute="get_custom_product_price",
            string="product_id"
    )

    @api.model
    def _get_product_id(self):
        product_id = False
        if self.env.context.get('product_template_id', False):
            product_tmpl = self.env['product.template'].browse(
                    [self.env.context.get('product_template_id')]
            )
            product_id = False
            if product_tmpl:
                product_tmpl_id = product_tmpl[0]
                if product_tmpl_id and product_tmpl_id.product_variant_ids:
                    product = product_tmpl_id.product_variant_ids[0]
                    if product:
                        product_id = product.id
        elif self.env.context.get('product_id', False):
            product_id = self.env.context.get('product_id')

        return product_id

    def get_custom_product_price(self):
        for rec in self:
            rec._get_custom_product_price()

    def _get_custom_product_price(self):
        product_id = self._get_product_id()
        if product_id:
            product = self.env['product.product'].browse([product_id])
            self.product_price = self._price_get(product, 1).get(self.id, 0.0)
            self.product_id = product_id

    def _set_custom_product_price(self):
        # Real change takes place in price_set after inverse
        # method of pricelists object on product_template
        _logger.debug("Set Price: %s", self.product_price)

    def remove_price_manual(self):
        for rec in self:
            rec._remove_price_manual()

    def _remove_price_manual(self):
        # Real change takes place in price_set after inverse
        # method of pricelists object on product_template
        if self._context.get('product_template_id'):
            self.price_remove(self._context.get('product_template_id'))
        if self._context.get('product_id'):
            product = self.env['product.product'].browse(self._context.get('product_id'))
            self.price_remove(product.product_tmpl_id.id)

    def price_set(self, product_template, new_price):
        """
        Set the price of the product in current pricelist
        if different from price through  pricerules
        :param product_template: product_template object
        :param new_price: new price
        :return:
        """
        if new_price:
            items = self.env['product.pricelist.item'].search(
                    [
                        ('product_tmpl_id','=', product_template.id),
                        ('pricelist_id', '=', self.id)
                    ]
            )
            product_price_type_ids = self.env['product.pricelist.item'].search(
                [
                    ('base', '=', 'list_price')
                ]
            )
            if not items:
                self.env['product.pricelist.item'].create(
                    {
                        'base': 'list_price',  # product_price_type_ids and product_price_type_ids[0].id,
                        'sequence': 1,
                        'name': product_template.name,
                        'product_tmpl_id': product_template.id,
                        'pricelist_id': self.id,
                        'fixed_price': new_price,
                        'price_discount': -1
                    }
                )
            else:
                for item in items:
                    item.write(
                        {
                            'base': 'list_price',  # product_price_type_ids and product_price_type_ids[0].id,
                            'sequence': 1,
                            'name': product_template.name,
                            'product_tmpl_id': product_template.id,
                            'pricelist_id': self.id,
                            'fixed_price': new_price,
                            'price_discount': -1
                        }
                    )
            return True

    @api.model
    def price_remove(self, product_template_id):
        items = self.env['product.pricelist.item'].search(
                    [
                        ('product_tmpl_id', '=', product_template_id)
                    ]
        )
        for item in items:
            item.unlink()

        return True
