# -*- coding: utf-8 -*-
# © 2004-2011 Tiny SPRL (<http://tiny.be>)
# © 2010-2011 Camptocamp Austria (<http://www.camptocamp.at>)
# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['abstract.ean', 'product.product']
