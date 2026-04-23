# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _reset_default_state(self):
        if default_state := self._get_default_product_state():
            self.write({"product_state_id": default_state.id})

    @api.model
    def cron_reset_shortage_states(self):
        """
        Finds products in a 'shortage' state that now have physical stock
        and resets them to the default state.
        """
        shortage_states = self.env["product.state"].search([("is_shortage", "=", True)])
        if not shortage_states:
            return

        templates = self.search([("product_state_id", "in", shortage_states.ids)])

        templates_to_reset = templates.filtered(
            lambda t: any(p.qty_available > 0 for p in t.product_variant_ids)
        )

        templates_to_reset._reset_default_state()
