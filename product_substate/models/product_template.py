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

    def _get_default_state_value(self):
        return self._get_default_product_state().code or "draft"

    def _update_before_write_create(self, values):
        # Users set ``product_state_id``; ``state`` is only computed from it.
        if (
            values.get("product_state_id")
            and not values.get("substate_id")
            and not values.get("state")
        ):
            state = self.env["product.state"].browse(values["product_state_id"])
            values["substate_id"] = self._get_default_substate_id(state.code)
        return super()._update_before_write_create(values)

    @api.constrains("substate_id", "state")
    def check_substate_id_value(self):
        # ``state`` is a Char holding the product state code: the mixin's
        # implementation relies on a selection field to build its message.
        if self.env.context.get("skip_substate_while_state_field_computation"):
            return
        for rec in self:
            # Read ``state`` first: flushing its pending recompute may itself
            # reset ``substate_id``.
            state = rec.state
            target_state = rec.substate_id.target_state_value_id.target_state_value
            if rec.substate_id and state != target_state:
                raise ValidationError(
                    self.env._(
                        "Substate %(substate_name)s not defined for "
                        "state %(state_name)s but for %(target_state_name)s",
                        substate_name=rec.substate_id.name,
                        state_name=rec.product_state_id.name,
                        target_state_name=rec.substate_id.target_state_value_id.name,
                    )
                )
