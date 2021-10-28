# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "tier.validation"]
    _tier_validation_manual_config = False

    @api.model
    def _is_tier_validated_active(self, state_code):
        return state_code != "draft"

    @api.model
    def create(self, vals):
        new = super().create(vals)
        if new.need_validation and self._is_tier_validated_active(new.state):
            new.active = False
        return new

    def write(self, vals):
        """
        Default `active` is False.
        It is set to True when State changes to confirmed.
        """
        if "state" in vals:
            vals["active"] = self._is_tier_validated_active(vals["state"])
        return super().write(vals)

    @api.model
    def _get_default_product_state_id(self):
        return self.env.ref(
            "product_state.demo_product_state_draft", raise_if_not_found=False
        )
