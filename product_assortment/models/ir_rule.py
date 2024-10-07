# Copyright 2024 Tecnativa - Sergio Teruel
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, tools
from odoo.osv import expression
from odoo.tools import config


class IrRule(models.Model):
    _inherit = "ir.rule"

    @api.model
    @tools.conditional(
        "xml" not in config["dev_mode"],
        tools.ormcache(
            "self.env.uid",
            "self.env.su",
            "model_name",
            "mode",
            "tuple(self._compute_domain_context_values())",
        ),
    )
    def _compute_domain(self, model_name, mode="read"):
        """Inject extra domain for restricting filter (Assortments) when the user
        has not the group 'Product Assortment Manager'.
        """
        res = super()._compute_domain(model_name, mode=mode)
        user = self.env.user
        if model_name == "ir.filters" and not self.env.su:
            if not user.has_group(
                "product_assortment.group_product_assortment_manager"
            ):
                extra_domain = [("is_assortment", "=", False)]
                extra_domain = expression.normalize_domain(extra_domain)
                res = expression.AND([extra_domain] + [res])
        return res
