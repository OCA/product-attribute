# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models
from odoo.tests import Form


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    def action_new_draft_picking_from_catalog(self):
        """Create a new draft picking from the catalog view"""
        picking_form = Form(
            self.env["stock.picking"].with_context(
                search_default_picking_type_id=self.ids,
                default_picking_type_id=self.id,
                contact_display="partner_address",
            )
        )
        picking = picking_form.save()
        action = picking.action_add_from_catalog()
        # So we can go back safely to the new picking instead of returning to the
        # previous screen
        action["target"] = "main"
        return action
