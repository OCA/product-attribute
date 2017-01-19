# -*- coding: utf-8 -*-
# © 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.addons.decimal_precision import decimal_precision as dp


class ProductPricelistSimulation(models.Model):
    _name = 'product.pricelist.simulation'

    @api.multi
    def _compute_price(self):
        for simulation in self:
            simulation.price = simulation.product_tmpl_id.with_context(
                pricelist=simulation.pricelist_id.id).price

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product',
        index=True,
    )
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        string='Pricelist',
        index=True,
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        related='pricelist_id.currency_id',
        string="Currency",
        readonly=True,
        required=True
    )
    price = fields.Monetary(
        compute=_compute_price,
        string='Price Simulated',
        digits=dp.get_precision('Product Price')
    )
    


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def _compute_pricelist_simulate_ids(self):
        res = self.env['product.pricelist.simulation']
        for template in self:
            pricelists = template.env['product.pricelist'].search([
                ('show_in_simulation', '=', True),
            ])
            simulations = self.env['product.pricelist.simulation'].search([
                ('product_tmpl_id', '=', template.id)
            ])
            for pricelist in pricelists:
                simulation = simulations.filtered(
                    lambda x: pricelist.id == x.pricelist_id.id)
                if not simulation:
                    res += simulation.create({
                        'product_tmpl_id': template.id,
                        'pricelist_id': pricelist.id,
                    })
                else:
                    res += simulation
            template.pricelist_simulate_ids = res

    pricelist_simulate_ids = fields.One2many(
        comodel_name='product.pricelist.simulation',
        inverse_name='product_tmpl_id',
        compute=_compute_pricelist_simulate_ids,
        string='Pricelist Simulate',
    )
