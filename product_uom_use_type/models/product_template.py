# -*- coding: utf-8 -*-
# Copyright 2017, Grap
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    uom_id = fields.Many2one(domain=[('use_type', 'in', ('sale', 'both'))])
    uom_po_id = fields.Many2one(domain=[
        ('use_type', 'in', ('purchase', 'both'))])

    @api.multi
    def onchange_uom(self, uom_id, uom_po_id):
        res = super(ProductTemplate, self).onchange_uom(uom_id, uom_po_id)
        if (uom_id and
                self.env['product.uom'].browse(uom_id).use_type != 'both'):
            if res.get('value', False):
                res['value']['uom_po_id'] = False
        return res
