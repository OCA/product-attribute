# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    lot_expiry_field_name = fields.Selection(
        compute="_compute_lot_expiry_field_name",
        selection="_selection_lot_expiry_field_name",
    )

    specific_lot_expiry_field_name = fields.Selection(
        selection="_selection_lot_expiry_field_name",
        help="Name of the field to use on a Lot/serial to determine if the "
        "lot is expired or not. If not provided, the one defined on the "
        "category is used",
    )

    category_lot_expiry_field_name = fields.Selection(
        related="categ_id.lot_expiry_field_name", readonly=True,
    )

    @api.model
    def _selection_lot_expiry_field_name(self):
        return self.env["stock.production.lot"]._selection_expiry_date_field()

    @api.depends(
        "specific_lot_expiry_field_name", "category_lot_expiry_field_name"
    )
    def _compute_lot_expiry_field_name(self):
        for rec in self:
            rec.lot_expiry_field_name = (
                rec.specific_lot_expiry_field_name
                or rec.category_lot_expiry_field_name
            )
