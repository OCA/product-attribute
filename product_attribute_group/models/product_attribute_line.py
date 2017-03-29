# -*- coding: utf-8 -*-
# Copyright 2017 OCA - Odoo Community Association
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProductAttributeLine(models.Model):

    _inherit = 'product.attribute.line'

    name = fields.Char()
    attr_group_ids = fields.Many2many(
        comodel_name='product.attribute.group',
        string='Attribute Groups',
        domain=lambda s: [('attribute_id', '=', s.attribute_id.id)]
        )
    orig_attr_group_ids = fields.Many2many(
        comodel_name='product.attribute.group',
        string='Original Attribute Groups',
        relation='product_tmpl_orig_attr_group_rel',
        domain=lambda s: [('attribute_id', '=', s.attribute_id.id)]
        )


    @api.onchange('attr_group_ids')
    def onchange_attr_group(self):
        """
        First we remove all the values belonging
        to the original attribute group then add in
        the new ones.
        :return: 
        """
        values = self.value_ids
        removed_attr_groups = (self._origin.attr_group_ids -
                               self.attr_group_ids)
        for origin_attr_group in removed_attr_groups:
            if origin_attr_group not in self.attr_group_ids:
                values -= origin_attr_group.value_ids
        for attr_group in self.attr_group_ids:
            values |= attr_group.value_ids
        self._origin.attr_group_ids = self.attr_group_ids
        self.value_ids = values

    @api.multi
    def button_clear_values(self):
        for attr_line in self:
            attr_line.value_ids = self.env['product.attribute.value']
            attr_line.attr_group_ids = self.env['product.attribute.group']
