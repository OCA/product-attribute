# Copyright 2026 AGF Vector GmbH (<https://agfvector.at>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def action_confirm(self):
        self._check_product_state_restriction()
        return super().action_confirm()

    def button_mark_done(self):
        self._check_product_state_restriction()
        return super().button_mark_done()

    def pre_button_mark_done(self):
        self._check_product_state_restriction()
        return super().pre_button_mark_done()

    def _check_product_state_restriction(self):
        for mo in self:
            # Finished product
            state = mo.product_id.product_tmpl_id.product_state_id
            if state and state.restrict_manufacture:
                raise UserError(
                    self.env._(
                        "Product '%(product)s' is in state '%(state)s' and cannot"
                        " be manufactured.\n"
                        "Manufacturing Order: %(mo)s",
                        product=mo.product_id.display_name,
                        state=state.name,
                        mo=mo.name,
                    )
                )

            # Components (raw materials)
            for move in mo.move_raw_ids.filtered(lambda m: m.state != "cancel"):
                c_state = move.product_id.product_tmpl_id.product_state_id
                if c_state and c_state.restrict_manufacture:
                    raise UserError(
                        self.env._(
                            "Component '%(product)s' is restricted for manufacturing "
                            "(state: %(state)s).\nManufacturing Order: %(mo)s",
                            product=move.product_id.display_name,
                            state=c_state.name,
                            mo=mo.name,
                        )
                    )
