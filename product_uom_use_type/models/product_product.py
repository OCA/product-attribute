# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.onchange("uom_id")
    def _onchange_uom_id(self):
        # If it's an UoM dedicated to sale, We can't set is as uom_po_id
        # So prevent to call super(), but check if categories are consistent
        if self.uom_id.use_type == "sale":
            if self.uom_id.category_id != self.uom_po_id.category_id:
                self.uom_po_id = False
            return
        return super()._onchange_uom_id()

    @api.onchange("uom_po_id")
    def _onchange_uom(self):
        # If it's an PO UoM dedicated to purchase, We can't set is as uom_sid
        # So prevent to call super(), but check if categories are consistent
        if self.uom_po_id.use_type == "purchase":
            if self.uom_id.category_id != self.uom_po_id.category_id:
                self.uom_id = False
            return
        return super()._onchange_uom()
