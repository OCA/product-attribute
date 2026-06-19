# Copyright (C) 2026 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.tools.float_utils import float_compare


class ChooseDeliveryPackage(models.TransientModel):
    _inherit = "choose.delivery.package"

    def _compute_shipping_weight(self):
        super()._compute_shipping_weight()
        for rec in self:
            move_line_ids = rec.picking_id.move_line_ids.filtered(
                lambda m: float_compare(
                    m.qty_done, 0.0, precision_rounding=m.product_uom_id.rounding
                )
                > 0
                and not m.result_package_id
                and not m.product_id.weight
                and m.product_id.product_tmpl_id.weight
            )
            if not move_line_ids:
                continue
            for ml in move_line_ids:
                qty = ml.product_uom_id._compute_quantity(
                    ml.qty_done, ml.product_id.uom_id
                )
                rec.shipping_weight += qty * ml.product_id.product_tmpl_id.weight
        return True
