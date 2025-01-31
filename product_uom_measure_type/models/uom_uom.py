# Copyright (C) 2022 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class UomUom(models.Model):
    _inherit = "uom.uom"

    measure_type = fields.Selection(
        string="Type of Measure",
        related="category_id.measure_type",
        store=True,
        readonly=True,
    )
