# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "tier.validation"]
    _tier_validation_manual_config = False

    def _check_state_conditions(self, vals):
        """
        As product state write is done on product_state_id field if
        changed through interface. We need to get the correspondong state
        """
        self.ensure_one()
        if "product_state_id" in vals:
            new_state = self.env["product.state"].browse(vals["product_state_id"]).code
            return (
                getattr(self, self._state_field) in self._state_from
                and new_state in self._state_to
            )
        else:
            return super()._check_state_conditions(vals)

    def _check_tier_state_transition(self, vals):
        """
        As product state write is done on product_state_id field if
        changed through interface. We need to get the correspondong state
        """
        self.ensure_one()
        if "product_state_id" in vals:
            new_state = self.env["product.state"].browse(vals["product_state_id"]).code
            return getattr(
                self, self._state_field
            ) in self._state_from and new_state not in (
                self._state_to + [self._cancel_state]
            )
        else:
            return super()._check_tier_state_transition(vals)
