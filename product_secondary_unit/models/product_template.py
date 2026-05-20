# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    secondary_uom_ids = fields.One2many(
        comodel_name="product.secondary.unit",
        inverse_name="product_tmpl_id",
        string="Secondary Unit of Measure",
        help="Default Secondary Unit of Measure.",
        context={"active_test": False},
    )

    @api.model
    def _get_default_secondary_uom(self):
        return (
            self.secondary_uom_ids
            and self.secondary_uom_ids[0]
            or self.secondary_uom_ids
        )
