# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductApplication(models.Model):
    _name = 'product.application'
    _inherit = [_name, 'custom.info']

    custom_info_template_id = fields.Many2one(
        context={"default_model": _name})
    custom_info_ids = fields.One2many(
        context={"default_model": _name})

    name = fields.Char(
        string='Application Name',
        compute='_get_application_name',
        required=False
    )

    def _get_custom_info_name_value_pairs(self):
        self.ensure_one()

        pairs = []
        custom_infos = sorted(self.custom_info_ids, key=lambda x: x.property_id.sequence)
        for info in custom_infos:
            cur_value = False
            if info.field_name == 'value_int':
                cur_value = info.value_int
            elif info.field_name == 'value_bool':
                cur_value = info.value_bool
            elif info.field_name == 'value_float':
                cur_value = info.value_float
            elif info.field_name == 'value_str':
                cur_value = info.value_str
            elif info.value:
                cur_value = str(info.value)
            else:
                cur_value = False
            pairs.append((info.name, str(cur_value)))
        return pairs

    @api.model
    def _get_application_name(self):
        for app in self:
            pairs = app._get_custom_info_name_value_pairs()
            if pairs:
                values = []
                for pair in pairs:
                    values.append(pair[1])
                app.name = ' | '.join(values)
