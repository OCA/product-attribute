# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    uom_measure_type = fields.Selection(
        string="UoM Type of Measure",
        related="uom_id.measure_type",
        store=True,
        readonly=True,
    )
