# -*- coding: utf-8 -*-
# Copyright 2019 Callino

from odoo import api, fields, models, tools, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    variant_item_ids = fields.One2many('product.pricelist.item', 'product_id', 'Pricelist Items')
