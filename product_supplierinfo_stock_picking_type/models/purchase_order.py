# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange("picking_type_id")
    def onchange_picking_type_id_onchange_product(self):
        # Method name is to avoid conflicts with mrp_subcontracting_dropshipping
        # that have an onchange method named onchange_picking_type_id
        for line in self.order_line:
            line.onchange_product_id()
