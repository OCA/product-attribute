# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from odoo.exceptions import ValidationError


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
