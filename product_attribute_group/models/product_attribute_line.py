# -*- coding: utf-8 -*-
# Copyright 2017 OCA - Odoo Community Association
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductAttributeLine(models.Model):

    _inherit = 'product.attribute.line'

    name = fields.Char()
    attr_group_ids = fields.Many2many(
        comodel_name='product.attribute.group',
        string='Attribute Groups',
        domain=lambda s: [('attribute_id', '=', s.attribute_id.id)]
        )

    @api.onchange('attr_group_ids')
    def onchange_attr_group(self):
        """
        Mostly eye candy - we update the display to show the new values
        when the attribute group changes - however as the field is
        readonly in the UI it won't write so we handle properly in write
        :return:
        """
        self.value_ids = self.attr_group_ids.mapped('value_ids')

    @api.multi
    def write(self, vals):
        """
        Override write in order to ensure that values match
        the group.
        :param vals:
        :return:
        """
        if 'attr_group_ids' in vals:
            if vals.get('attr_group_ids'):
                attr_groups = self.env['product.attribute.group'].browse(
                    vals['attr_group_ids'][0][2])
                vals['value_ids'] = [
                    [6, False, attr_groups.mapped('value_ids').ids]]
            else:
                vals['value_ids'] = []
        return super(ProductAttributeLine, self).write(vals)
