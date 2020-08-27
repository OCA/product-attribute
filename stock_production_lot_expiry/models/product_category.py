# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductCategory(models.Model):

    _inherit = "product.category"

    lot_expiry_field_name = fields.Selection(
        compute="_compute_lot_expiry_field_name",
        selection="_selection_lot_expiry_field_name",
    )

    specific_lot_expiry_field_name = fields.Selection(
        selection="_selection_lot_expiry_field_name",
        help="Name of the field to use on a Lot/serial to determine if the "
        "lot is expired or not. If not provided, the one defined on the "
        "parent is used. In the case where this field is not defined into"
        "the hierarchy, the default one specified into the stock "
        "settings is used.",
    )

    parent_lot_expiry_field_name = fields.Selection(
        selection="_selection_lot_expiry_field_name",
        compute="_compute_parent_lot_expiry_field_name",
        store=True,
        readonly=True,
    )

    @api.model
    def _selection_lot_expiry_field_name(self):
        return self.env["stock.production.lot"]._selection_expiry_date_field()

    @api.depends(
        "specific_lot_expiry_field_name", "parent_lot_expiry_field_name"
    )
    def _compute_lot_expiry_field_name(self):
        default_value = self.env[
            "stock.config.settings"
        ].get_production_lot_expiry_date_field()
        for rec in self:
            rec.lot_expiry_field_name = (
                rec.specific_lot_expiry_field_name
                or rec.parent_lot_expiry_field_name
                or default_value
            )

    @api.depends(
        "parent_id.specific_lot_expiry_field_name",
        "parent_id.parent_lot_expiry_field_name",
    )
    def _compute_parent_lot_expiry_field_name(self):
        for rec in self:
            parent_id = rec.parent_id
            rec.parent_lot_expiry_field_name = (
                parent_id.specific_lot_expiry_field_name
                or parent_id.parent_lot_expiry_field_name
            )
