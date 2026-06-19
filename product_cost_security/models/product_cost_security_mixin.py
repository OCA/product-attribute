# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)
import re
from contextlib import suppress

from lxml import etree

from odoo import api, fields, models
from odoo.exceptions import AccessError

_STANDARD_PRICE_RE = re.compile(r"\bstandard_price\b")
_EXPR_ATTRS = ("context", "invisible", "readonly", "required", "column_invisible")

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
    def check_field_access_rights(self, operation, fields):
        """Forbid users from updating product costs if they have no permissions.

        The field's `groups` attribute restricts always R/W access. We apply an
        extra protection to prevent only editing if the user is not in the
        `product_cost_security.group_product_edit_cost` group.
        """
        valid_fields = super().check_field_access_rights(operation, fields)
        if self.env.su:
            return valid_fields
        product_cost_fields = self._product_cost_security_fields().intersection(
            valid_fields
        )
        if (
            operation != "read"
            and product_cost_fields
            and not self._user_can_update_cost()
        ):
            description = self.env["ir.model"]._get(self._name).name
            raise AccessError(
                self.env._(
                    'You do not have enough rights to access the fields "%(fields)s"'
                    " on %(document_kind)s (%(document_model)s). "
                    "Please contact your system administrator."
                    "\n\n(Operation: %(operation)s)",
                    fields=",".join(sorted(product_cost_fields)),
                    document_kind=description,
                    document_model=self._name,
                    operation=operation,
                )
            )
        return valid_fields

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Make product cost fields readonly for non-editors."""
        result = super().fields_get(allfields, attributes)
        if not self._user_can_update_cost():
            for field_name in self._product_cost_security_fields():
                with suppress(KeyError):
                    result[field_name]["readonly"] = True
        return result

    @api.model
    def _product_cost_security_strip_arch(self, arch_str):
        """Hide cost fields and sanitize view expressions for users without access."""
        tree = etree.fromstring(arch_str.encode() if isinstance(arch_str, str) else arch_str)
        changed = False

        for xpath in ("//field[@name='standard_price']", "//label[@for='standard_price']"):
            for node in tree.xpath(xpath):
                parent = node.getparent()
                if parent is not None:
                    parent.remove(node)
                    changed = True

        for node in tree.iter():
            for attr in _EXPR_ATTRS:
                value = node.get(attr)
                if value and _STANDARD_PRICE_RE.search(value):
                    new_value = _STANDARD_PRICE_RE.sub("0", value)
                    if new_value != value:
                        node.set(attr, new_value)
                        changed = True

        if not changed:
            return arch_str
        return etree.tostring(tree, encoding="unicode").replace("\t", "")

    @api.model
    def _product_cost_security_strip_view_models(self, models_data):
        if isinstance(models_data, dict):
            cleaned = {}
            for model_name, model_fields in models_data.items():
                fields_set = set(model_fields)
                fields_set.discard("standard_price")
                cleaned[model_name] = tuple(fields_set)
            return cleaned
        return models_data

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id, view_type, **options)
        if self.env.user.has_group("product_cost_security.group_product_cost"):
            return result
        result = dict(result)
        if result.get("arch"):
            result["arch"] = self._product_cost_security_strip_arch(result["arch"])
        if result.get("models"):
            result["models"] = self._product_cost_security_strip_view_models(
                dict(result["models"])
            )
        return result
