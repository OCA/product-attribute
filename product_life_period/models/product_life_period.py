# -*- coding: utf-8 -*-
# © 2015  Laetitia Gangloff, Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductLifePeriod(models.Model):
    _name = 'product.life.period'

    name = fields.Char(translate=True)
    start_date = fields.Date()
    end_date = fields.Date(index=True)
    active = fields.Boolean(default=True)
    product_ids = fields.One2many('product.template', 'product_life_period_id',
                                  string='Seasonal Products', index=True)
    products_count = fields.Integer(compute='_compute_products_count')

    @api.one
    @api.depends('product_ids')
    def _compute_products_count(self):
        self.products_count = len(self.product_ids)

    @api.multi
    def _run_life_period_update(self):
        """ At the end of life period, set product in state end
            And set the period inactive
        """
        product_template = self.env["product.template"]
        end_life_periods = self.search(
            [('end_date', '<=', fields.Date.today())])
        end_life_product_ids = set()
        for end_life_period in end_life_periods:
            end_life_product_ids = end_life_product_ids.union(
                end_life_period.product_ids.ids)
        product_template.browse(end_life_product_ids).write({'state': 'end'})
        end_life_periods.write({'active': False})
        return True

    @api.multi
    def _check_date(self):
        """ Check state date is before end date
        """
        for life_period in self:
            if life_period.start_date and life_period.end_date:
                return life_period.start_date < life_period.end_date
        return True

    _constraints = [
        (_check_date,
         'Start date must be before End date', ['start_date', 'end_date'])]
