# -*- coding: utf-8 -*-
# © 2015 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api


class ProductUom(models.Model):
    _inherit = 'product.uom'

    weight_volumetric_ratio = fields.Float(
        'Volumetric Weight Ratio (Kg/m3)',
        help="Used as variable for the volumetric weight calculation "
        "using the formula. (Volume * Ratio) = Kg",
        default=100)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    @api.depends('dimensional_uom_id', 'volume')
    def _get_volumetric_weight(self):
        for product in self:
            product.weight_volumetric = (
                product.volume *
                product.dimensional_uom_id.weight_volumetric_ratio)

    weight_volumetric = fields.Float(
        string='Volumetric weight', compute="_get_volumetric_weight",
        store=True, readonly=True)
