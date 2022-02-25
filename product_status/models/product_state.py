# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv import expression


class ProductState(models.Model):
    _inherit = "product.state"

    def write(self, vals):
        allow = {"default", "active"}
        if not allow.issuperset(set(vals)):
            self._check_module_data()
        return super().write(vals)

    def unlink(self):
        self._check_module_data()
        return super().unlink()

    def _check_module_data(self):
        if self.env.user.id == 1:
            return True
        default_data = [st.code for st in self._get_module_data()]
        msg = _("Cannot delete/modified state installed by module, state name: %s")
        for rec in self:
            if rec.code in default_data:
                raise ValidationError(msg % rec.name)

    def _get_module_data(self):
        code = ["new", "discontinued", "phaseout", "endoflife"]
        return self.env["product.state"].search([("code", "in", code)])

    @api.model
    def _domain_recompute_product_state(self):
        today = fields.Date.today()
        return expression.OR(
            [
                # get 'phaseout' products that should be updated to 'endoflife'
                [
                    ("end_of_life_date", "!=", False),
                    ("end_of_life_date", "<", today),
                    ("state", "=", "phaseout"),
                ],
                # discontinued
                [
                    ("discontinued_until", "!=", False),
                    ("discontinued_until", "<", today),
                    ("state", "=", "discontinued"),
                ],
                # get products that aren't 'new' anymore
                [
                    ("new_until", "!=", False),
                    ("new_until", "<", today),
                    ("state", "=", "new"),
                ],
            ]
        )

    @api.model
    def _get_products_recompute_product_state(self):
        domain = self._domain_recompute_product_state()
        templates = (
            self.env["product.template"].with_context(active_test=False).search(domain)
        )
        variants = (
            self.env["product.product"].with_context(active_test=False).search(domain)
        )
        return templates, variants

    @api.model
    def _cron_recompute_product_state(self):
        """Recompute the state of products."""
        templates, variants = self._get_products_recompute_product_state()
        for template in templates:
            template._check_dates_of_states(template)
        for variant in variants:
            variant.product_tmpl_id._check_dates_of_states(variant)
        return bool(templates or variants)
