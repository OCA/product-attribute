# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    uom_category_id = fields.Many2one(
        comodel_name="uom.category", related="uom_id.category_id")

    # Overload field to add a domain
    uom_po_id = fields.Many2one(
        domain="[('category_id', '=', uom_category_id)]"
    )
