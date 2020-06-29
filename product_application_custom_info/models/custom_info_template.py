# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CustomInfoTemplate(models.Model):
    _inherit = "custom.info.template"
    _order = "model_id, name"

    @api.model
    def _default_model_id(self):
        model_obj = self.env['ir.model']

        if self._context.get('default_model', False):
            default_model = model_obj.search([
                ('model', '=', self._context['default_model'])])
            if default_model:
                return default_model.id
        return 0
#     )
    model_id = fields.Many2one(
        comodel_name='ir.model', string='Model', ondelete="restrict",
        required=True, auto_join=True,
        default=_default_model_id
    )
