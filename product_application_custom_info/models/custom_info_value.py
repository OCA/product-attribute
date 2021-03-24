# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval


class CustomInfoValue(models.Model):
    _description = "Custom information value"
    _inherit = "custom.info.value"

    value = fields.Char(
        compute="_compute_value",
        search="_search_value",
        help="Value, always converted to/from the typed field.",
        inverse="_inverse_value",
    )

    @api.multi
    def _inverse_value(self):
        """Store the owner according to the model and ID."""
        for info_value in self:
            property = info_value.property_id
            if property.field_type == 'str':
                info_value.value_str = info_value.value
            elif property.field_type == 'int':
                info_value.value_int = int(info_value.value)
            elif property.field_type == 'float':
                info_value.value_float = float(info_value.value)
            elif property.field_type == 'bool':
                if info_value.value in ('0', 'f', 'false', 'False', 'FALSE'):
                    info_value.value_bool = False
                else:
                    info_value.value_bool = True
            elif property.field_type == 'date':
                info_value.value_date = int(info_value.value)
