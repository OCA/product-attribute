# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)
from contextlib import suppress

from odoo import api, fields, models
from odoo.exceptions import AccessError


class ProductCostSecurityMixin(models.AbstractModel):
    """Automatic security for models related with product costs.

    When you inherit from this mixin, make sure to add
    `groups="product_cost_security.group_product_cost"` to the fields that
    should be protected. Odoo will take care of hiding those fields to users
    without that access, and this mixin will add an extra protection to prevent
    editing if the user is not in the
    `product_cost_security.group_product_edit_cost` group.
    """

    _name = "product.cost.security.mixin"
    _description = "Product cost access control mixin"

    user_can_update_cost = fields.Boolean(compute="_compute_user_can_update_cost")

    @api.depends_context("uid")
    def _compute_user_can_update_cost(self):
        """Let views know if users can edit product costs.

        A user could have full cost permissions but no product edition permissions.
        We want to prevent those from updating costs.
        """
        self.user_can_update_cost = self._user_can_update_cost()

    @api.model
    def _user_can_update_cost(self):
        """Know if current user can update product costs.

        Just like `self.user_can_update_cost`, but once per model.
        """
        return self.env.user.has_group("product_cost_security.group_product_edit_cost")

    @api.model
    def _product_cost_security_fields(self):
        """Fields that should be hidden if the user has no cost permissions.

        Returns a list of field names where the security group is applied.
        """
        return {
            fname
            for (fname, field) in self._fields.items()
            if "product_cost_security.group_product_cost"
            in str(field.groups).split(",")
        }

    @api.model
    def _check_field_access(self, field, operation):
        # Forbid users from updating product costs if they have no permissions.
        # Odoo 19.0 enforces field access through this method during read/write
        # operations, so the edit restriction must be applied here too.
        super()._check_field_access(field, operation)
        if self.env.su:
            return
        if (
            operation != "read"
            and field.name in self._product_cost_security_fields()
            and not self._user_can_update_cost()
        ):
            raise AccessError(
                self.env._(
                    "You do not have enough rights to update product costs. "
                    "Please contact your system administrator."
                )
            )

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        # Make product cost fields readonly for non-editors.
        result = super().fields_get(allfields, attributes)
        if not self._user_can_update_cost():
            for field_name in self._product_cost_security_fields():
                with suppress(KeyError):
                    result[field_name]["readonly"] = True
        return result
