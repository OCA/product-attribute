# Copyright 2024 Tecnativa - Pilar Vargas
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import _, exceptions, models


class FakeProductSetWizard(models.Model):
    _name = "fake.product.set.wizard"
    _inherit = "product.set.wizard"
    _description = "Product set wizard fake for test"

    def _check_partner(self):
        if not self.product_set_id.partner_id:
            return
        if self.partner_id != self.product_set_id.partner_id:
            raise exceptions.ValidationError(
                _("This set of products is restricted for this user.")
            )
