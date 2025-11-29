# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BaseSubstateType(models.Model):
    _inherit = "base.substate.type"

    model = fields.Selection(
        selection_add=[("product.template", "Product")],
        ondelete={"product.template": "cascade"},
    )


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "base.substate.mixin"]
    _state_field = "product_state_id"

    # Computed field to access the product state code for domain filtering
    product_state_code = fields.Char(
        compute="_compute_product_state_code",
        store=False,
        search="_search_product_state_code",
    )

    @api.depends("product_state_id.code")
    def _compute_product_state_code(self):
        for record in self:
            product_state_id = record.product_state_id
            record.product_state_code = (
                product_state_id.code if product_state_id else False
            )

    def _search_product_state_code(self, operator, value):
        # This allows domain filtering based on the related code
        return [("product_state_id.code", operator, value)]

    @api.constrains("substate_id", "product_state_id")
    def check_substate_id_value(self):
        if not self._state_field:
            return
        for rec in self:
            if not rec.substate_id or not rec[self._state_field]:
                continue
            current_state_code = rec[self._state_field].code
            substate = rec.substate_id
            target_state_value = substate.target_state_value_id.target_state_value
            if target_state_value != current_state_code:
                raise ValidationError(
                    self.env._("The substate is not valid for the current state.")
                )
