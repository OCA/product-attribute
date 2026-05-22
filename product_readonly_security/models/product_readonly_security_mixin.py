# Copyright 2024-2026 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import functools

from odoo import models
from odoo.tools import config


class ProductReadonlySecurityMixin(models.AbstractModel):
    _name = "product.readonly.security.mixin"
    _description = "Mixin to use Product Readonly Security"

    def _check_access(self, operation):
        # We override this method directly because we want to display an error
        # (similar to what happens if a user don't have access -ACL- to perform
        # an action on a model) if the user does not have the "Product edition" group.
        # This method is very useful because it helps ensure that the Create/Edit/Delete
        # buttons are not displayed across all sections of Odoo, including in many2one
        # fields (example: the product field in sales order lines).
        user = self.env.user
        group = "product_readonly_security.group_product_edition"
        test_condition = not config["test_enable"] or (
            config["test_enable"]
            and self.env.context.get("test_product_readonly_security")
        )
        if (
            test_condition
            and operation != "read"
            and not self.env.su
            and not user.has_group(group)
        ):
            # Similar to https://github.com/odoo/odoo/blob/4b62fa9ba12d0ef40671d31bb33c6eeffda5cd85/odoo/models.py#L4477
            Access = self.env["ir.model.access"]
            return self, functools.partial(
                Access._make_access_error, self._name, operation
            )
        return super()._check_access(operation)
