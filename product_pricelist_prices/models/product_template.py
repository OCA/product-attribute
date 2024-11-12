# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    latest_purchase_price_id = fields.Monetary(string="Latest Purchase Price", default=0, compute="_compute_latest_purchase_price_id")

    def _compute_latest_purchase_price_id(self):
        for rec in self:
            _logger.info("NUMERO DE IDS,%s", rec.product_variant_ids)
            if len(rec.product_variant_ids) < 2:
                rec.latest_purchase_price_id = rec.product_variant_ids.latest_purchase_price
            else :
                rec.latest_purchase_price_id = 0

    def get_pricelists(self):
        for rec in self:
            rec._get_pricelists()

    def _get_pricelists(self):
        self.pricelists = self.env['product.pricelist'].search(
                [
                    ('show_on_products', '=', True)
                ]
        )

    def _set_pricelists(self):
        for pricelist in self.pricelists:
            if pricelist.product_price:
                pricelist.price_set(self, pricelist.product_price)

    pricelists = fields.One2many(
            comodel_name="product.pricelist",
            string="Pricelists",
            compute="get_pricelists",
            inverse="_set_pricelists"
    )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    latest_purchase_price = fields.Monetary(string="Latest Purchase Price", default=0,
                                            compute="latest_purchase_price_compute")

    @api.depends("latest_purchase_price")
    def latest_purchase_price_compute(self):
        sale = self.env['account.move'].search([('invoice_line_ids.product_id', '=', self.ids),
                                                ('state', '=', 'posted'), ('move_type', '=', 'in_invoice')],
                                               order='invoice_date desc')
        set_price = False
        for rec in self:
            if sale.invoice_line_ids:
                for sales in sale:
                    if set_price == True:
                        break
                    sale_id = sales.invoice_line_ids
                    for line in sale_id:
                                if line.product_id.ids == self.ids:
                                    if line.quantity > 0:
                                        rec.latest_purchase_price = line.price_unit
                                        set_price = True
                                    elif line.quantity <= 0 and sales == sale[-1]:
                                        rec.latest_purchase_price = rec.standard_price
                                        set_price = True
                                    else:
                                        continue
            else:
                rec.latest_purchase_price = rec.standard_price
