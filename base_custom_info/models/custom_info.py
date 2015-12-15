# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models, _


class CustomInfoTemplate(models.Model):
    _name = "custom.info.template"
    _description = "Template of properties"

    name = fields.Char()
    model_id = fields.Many2one(comodel_name='ir.model', string='Data Model')
    info_ids = fields.One2many(
        comodel_name='custom.info.property',
        inverse_name='template_id',
        string='Properties')


class CustomInfoProperty(models.Model):
    """Name of the custom information property."""
    _name = "custom.info.property"
    _description = "Custom information property"

    name = fields.Char()
    template_id = fields.Many2one(
        comodel_name='custom.info.template',
        string='Template')
    info_value_ids = fields.One2many(
        comodel_name="custom.info.value",
        inverse_name="property_id",
        string="Property Values")


class CustomInfoValue(models.Model):
    _name = "custom.info.value"
    _description = "Values of properties"
    _rec_name = 'value'

    model = fields.Char(index=True, required=True)
    res_id = fields.Integer(index=True, required=True)
    property_id = fields.Many2one(
        comodel_name='custom.info.property',
        required=True,
    value = fields.Char()
        string='Property')
    name = fields.Char(related='property_id.name')


class CustomInfo(models.AbstractModel):
    _name = "custom.info"
    _description = "Abstract model from inherit to add info in any model"

    custom_info_template_id = fields.Many2one(
        comodel_name='custom.info.template',
        string='Property Template')
    custom_info_ids = fields.One2many(
        comodel_name='custom.info.value',
        inverse_name='res_id',
        domain=lambda self: [('model', '=', self._name)],
        auto_join=True,
        string='Custom Properties')

    @api.onchange('custom_info_template_id')
    def _onchange_custom_info_template_id(self):
        if not self.custom_info_template_id:
            self.custom_info_ids = False
        else:
            info_list = self.custom_info_ids.mapped('property_id')
            for info_name in self.custom_info_template_id.info_ids:
                if info_name not in info_list:
                    self.custom_info_ids |= self.custom_info_ids.new({
                        'model': self._name,
                        'property_id': info_name.id,
                    })

    @api.multi
    def unlink(self):
        info_values = self.mapped('custom_info_ids')
        res = super(CustomInfo, self).unlink()
        if res:
            info_values.unlink()
        return res
