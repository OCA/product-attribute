# Copyright 2024 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)
import re
from contextlib import suppress

from lxml import etree

from odoo import api, fields, models

_STANDARD_PRICE_RE = re.compile(r"\bstandard_price\b")
_EXPR_ATTRS = ("context", "invisible", "readonly", "required", "column_invisible")
_EXTRA_COST_FIELD_NAMES = frozenset(
    {
        "fc_standard_price",
        "fc_avg_cost",
        "fc_total_value",
        "avg_cost",
        "total_value",
        "alt_cost_foreign_currency",
    }
)

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
    def _product_cost_security_extra_fields(self):
        """Cost-like fields from other modules without field-level groups."""
        return _EXTRA_COST_FIELD_NAMES.intersection(self._fields)

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
    def _has_field_access(self, field, operation):
        """Extend Odoo 19 field ACLs for Kreilabs cost-like fields."""
        if not super()._has_field_access(field, operation):
            return False
        if self.env.su:
            return True
        if field.name in self._product_cost_security_extra_fields():
            if not self.env.user.has_group("product_cost_security.group_product_cost"):
                return False
        if (
            operation == "write"
            and field.name in self._product_cost_security_fields()
            and not self._user_can_update_cost()
        ):
            return False
        return True

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
    def _product_cost_security_protected_field_names(self):
        return {"standard_price", *self._product_cost_security_extra_fields()}

    @api.model
    def _product_cost_security_strip_arch(self, arch_str):
        """Hide cost fields and sanitize view expressions for users without access."""
        tree = etree.fromstring(arch_str.encode() if isinstance(arch_str, str) else arch_str)
        changed = False
        removed_fields = []

        for field_name in self._product_cost_security_protected_field_names():
            xpaths = (
                f"//field[@name='{field_name}']",
                f"//label[@for='{field_name}']",
                f"//div[@name='{field_name}_uom']",
            )
            for xpath in xpaths:
                for node in tree.xpath(xpath):
                    parent = node.getparent()
                    if parent is not None:
                        parent.remove(node)
                        changed = True
                        removed_fields.append(field_name)

        for node in tree.iter():
            for attr in _EXPR_ATTRS:
                value = node.get(attr)
                if value and _STANDARD_PRICE_RE.search(value):
                    new_value = _STANDARD_PRICE_RE.sub("0", value)
                    if new_value != value:
                        node.set(attr, new_value)
                        changed = True

        if not changed:
            return arch_str, removed_fields
        return etree.tostring(tree, encoding="unicode").replace("\t", ""), removed_fields

    @api.model
    def _product_cost_security_strip_view_models(self, models_data):
        if isinstance(models_data, dict):
            protected = self._product_cost_security_protected_field_names()
            cleaned = {}
            for model_name, model_fields in models_data.items():
                fields_set = set(model_fields) - protected
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
            result["arch"], _ = self._product_cost_security_strip_arch(result["arch"])
        if result.get("models"):
            result["models"] = self._product_cost_security_strip_view_models(
                dict(result["models"])
            )
        return result
