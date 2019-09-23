# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductCountryRestrictionItem(models.Model):

    _name = 'product.country.restriction.item'
    _description = 'Product Country Restriction Item'
    _order = 'sequence asc, id desc'

    name = fields.Char(
        compute='_compute_name',
        store=True,
        index=True,
    )
    sequence = fields.Integer(
        default=10,
    )
    restriction_id = fields.Many2one(
        comodel_name='product.country.restriction',
        index=True,
        ondelete='cascade',
    )
    rule_id = fields.Many2one(
        comodel_name='product.country.restriction.rule',
        string='Rule',
        required=True,
        ondelete='restrict',
    )
    rule_code = fields.Char(
        related='rule_id.code',
        readonly=True,
    )
    product_template_id = fields.Many2one(
        comodel_name='product.template',
        ondelete='cascade',
        index=True,
        string='Product',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        ondelete='cascade',
        index=True,
        string='Variant',
    )
    product_category_id = fields.Many2one(
        comodel_name='product.category',
        ondelete='cascade',
        index=True,
        string='Product Category',
    )
    start_date = fields.Date()
    end_date = fields.Date()

    @api.multi
    @api.depends(
        'start_date',
        'end_date',
        'restriction_id.name',
        'rule_id.name')
    def _compute_name(self):
        res = []
        for rec in self:
            dates = ''
            if rec.start_date and rec.end_date:
                dates = ' : '.join([rec.start_date, rec.end_date])
            params = [
                rec.restriction_id.name,
                rec.rule_id.name]
            if dates:
                params.append(dates)
            name = ' - '.join(params)
            rec.name = name
        return res

    @api.multi
    def _get_country_restriction_item_by_rule(self, products):
        """
        For one product apply one and just one item
        :param products:
        :return:
        """
        result = {}
        for item in self:
            res = item.rule_id._apply(products, item)
            for product in res:
                if product not in result:
                    result.update({
                        product: item,
                    })
        return result

    @api.multi
    @api.constrains('start_date', 'end_date')
    def _constrains_dates(self):
        if any(i.start_date > i.end_date for i in self
               if (i.start_date and i.end_date)):
            raise ValidationError(
                _('The start date cannot be greater than the end date!')
            )
