# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "tier.validation"]
    _state_from = ["draft", "cancel"]
    _state_to = ["confirmed"]
    _tier_validation_manual_config = False

    @api.depends("product_state_id")
    def _compute_product_state(self):
        # This module is incompatible with product_status so if its installed,
        # use its method. Otherwise update by state and not code.
        product_status_module = self.env["ir.module.module"].search(
            [["name", "=", "product_status"]]
        )
        for product_tmpl in self:
            if product_status_module and product_status_module.state == "installed":
                self._check_dates_of_states(product_tmpl)
            else:
                product_tmpl.state = product_tmpl.product_state_id.state

    @api.model
    def _set_product_state_id(self, record):
        # Overrides product state method since tier validation needs to look at state.
        # Backwards compatibility is built in else to satisfy other module unit tests.
        # This method can be called by variant so the record is either
        # product.template or product.product
        # The record param is for similar state field at product.product model.
        ProductState = record.env["product.state"]
        if record.state in ["draft", "confirmed", "cancel"]:
            product_state = ProductState.search([("state", "=", record.state)], limit=1)
            if not product_state:
                msg = _("The product state %s could not be found.")
                raise UserError(msg % record.state)
            if product_state.state != record.state:
                record.product_state_id = product_state.id
        else:
            product_state = ProductState.search([("code", "=", record.state)], limit=1)
            if record.state and not product_state:
                msg = _("The product state code %s could not be found.")
                raise UserError(msg % record.state)
            record.product_state_id = product_state.id

    def write(self, vals):
        # Tier Validation does not work with Stages, only States :-(
        # So, signal state transition by adding it to the vals
        # This module is incompatible with product_status so if its installed,
        # update state with code and not the state on the stage.
        if "product_state_id" in vals:
            stage_id = vals.get("product_state_id")
            stage = self.env["product.state"].browse(stage_id)
            product_status_module = self.env["ir.module.module"].sudo().search(
                [("name", "=", "product_status")]
            )
            if (
                stage.state in self._state_from
                or stage.state in self._state_to
                and not product_status_module
                or product_status_module.state != "installed"
                and stage.state != self.state
            ):
                vals["state"] = stage.state
            elif stage.code != self.state:
                vals["state"] = stage.code
        res = super().write(vals)
        if (
            "product_state_id" in vals
            and vals.get("product_state_id") in self._state_from
        ):
            self.restart_validation()
        return res
