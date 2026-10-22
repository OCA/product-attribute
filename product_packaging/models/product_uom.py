# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductUom(models.Model):
    _inherit = "product.uom"

    packaging_id = fields.Many2one(
        comodel_name="product.packaging",
        compute="_compute_packaging_id",
        store=True,
        index=True,
        ondelete="cascade",
    )

    @api.depends("product_id", "uom_id", "product_id.packaging_ids.uom_id")
    def _compute_packaging_id(self):
        for record in self:
            record.packaging_id = self.env["product.packaging"].search(
                [
                    ("product_id", "=", record.product_id.id),
                    ("uom_id", "=", record.uom_id.id),
                ],
                limit=1,
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("packaging_id") and not (
                vals.get("product_id") and vals.get("uom_id")
            ):
                packaging = self.env["product.packaging"].browse(vals["packaging_id"])
                vals.setdefault("product_id", packaging.product_id.id)
                vals.setdefault("uom_id", packaging.uom_id.id)
        return super().create(vals_list)

    @api.constrains("packaging_id", "product_id", "uom_id")
    def _check_packaging_uom(self):
        for record in self:
            if not record.packaging_id or not record.uom_id or not record.product_id:
                continue
            if record.packaging_id.uom_id != record.uom_id:
                raise ValidationError(
                    self.env._("The packaging UoM must match the UoM.")
                )
            if record.packaging_id.product_id != record.product_id:
                raise ValidationError(
                    self.env._("The packaging product must match the product.")
                )
