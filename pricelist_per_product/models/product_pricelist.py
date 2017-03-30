# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    product_template_count = fields.Integer(
        compute='_compute_product_template_count',
        string='Template with this Pricelist',
        help='Number of Product Template with this Pricelist',
    )
    product_item_ids = fields.One2many(
        comodel_name='product.pricelist.item',
        inverse_name='pricelist_id',
    )

    @api.multi
    def _compute_product_template_count(self):
        """ Count the number of ``product,template`` in the pricelist """
        total = self.item_ids.mapped('product_tmpl_id').ids
        self.product_template_count = len(total)

    @api.multi
    def button_template_in_pricelist(self):
        """ Return a tree form of ``product.template`` for the pricelist """
        self.ensure_one()
        pids = self.item_ids.mapped('product_tmpl_id').ids
        return {
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('id', 'in', pids)],
            'view_mode': 'tree,form',
            'res_model': 'product.template',
        }
