# -*- coding: utf-8 -*-
# © 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    show_in_simulation = fields.Boolean(
        string='Show this pricelist in simulation',
    )
