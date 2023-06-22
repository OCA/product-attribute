# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    uom_id = fields.Many2one(domain=[("use_type", "in", ("sale", "both"))])

    uom_po_id = fields.Many2one(domain=[("use_type", "in", ("purchase", "both"))])

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

    @api.constrains("uom_id", "uom_po_id")
    def _check_uom(self):
        if self.filtered(lambda x: x.uom_id.use_type == "purchase"):
            raise ValidationError(
                _("you can not set a 'Purchase' UoM as the main product UoM.")
            )
        if self.filtered(lambda x: x.uom_po_id.use_type == "sale"):
            raise ValidationError(
                _("you can not set a 'Sale' UoM as the product Purchase UoM.")
            )
        return super()._check_uom()
