# Copyright 2026 bosd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def copy(self, default=None):
        """Let an explicitly given internal reference reach the new variant.

        Odoo restores a ``default_code`` passed in ``default`` at the end of
        ``create()``, but only as long as the new template does not have one
        yet. As this module gives every new variant a number from the sequence,
        that is never the case and the given reference would be dropped. So
        hand it over to ``_prepare_variant_values()`` instead, which also
        avoids drawing a sequence number that nothing would ever use.
        """
        default = default or {}
        code = default.get("default_code")
        if code and code != "/":
            self = self.with_context(product_sequence_default_code=code)
        return super().copy(default=default)

    def _prepare_variant_values(self, combination):
        vals = super()._prepare_variant_values(combination)
        code = self.env.context.get("product_sequence_default_code")
        # An empty combination means the product has no attribute, hence a
        # single variant. Just like Odoo only propagates the reference of a
        # template to its variant when there is exactly one, the reference is
        # not copied over several variants, which all need their own.
        if code and not combination:
            vals["default_code"] = code
        return vals
