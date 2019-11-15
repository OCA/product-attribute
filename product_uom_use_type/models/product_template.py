# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT <quentin.dupont@grap.coop>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    uom_id = fields.Many2one(domain=[("use_type", "in", ("sale", "both"))])

    uom_po_id = fields.Many2one(
        domain=[("use_type", "in", ("purchase", "both"))]
    )

    @api.onchange("uom_id")
    def _onchange_uom_id(self):
        if self.uom_id.use_type != "sale":
            super(ProductTemplate, self)._onchange_uom_id()
