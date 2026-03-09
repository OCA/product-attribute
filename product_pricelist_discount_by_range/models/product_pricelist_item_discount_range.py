# Copyright 2026 Tecnativa - Andrii Kompaniiets
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductPricelistItemDiscountRange(models.Model):
    _name = "product.pricelist.item.discount_range"
    _description = "Product Pricelist Item Discount Range"

    pricelist_item_id = fields.Many2one(
        "product.pricelist.item", string="Pricelist Item", ondelete="cascade"
    )
    min = fields.Float(required=True)
    max = fields.Float(required=True)
    percentage = fields.Float(required=True)
    surcharge = fields.Float()

    _sql_constraints = [
        ("min_gt_max", "CHECK(min < max)", "Min value must be less than max value."),
    ]

    @api.constrains("min", "max", "percentage", "pricelist_item_id")
    def _check_ranges_overlap(self):
        for record in self:
            domain = [
                ("id", "!=", record.id),
                ("pricelist_item_id", "=", record.pricelist_item_id.id),
                ("min", "<=", record.max),
                ("max", ">=", record.min),
            ]
            overlap = self.search(domain, limit=1)
            if overlap:
                raise ValidationError(
                    self.env._(
                        "The discount range %(min)s - %(max)s "
                        "overlaps with an existing one %(overlap_min)s - "
                        "%(overlap_max)s.",
                        min=record.min,
                        max=record.max,
                        overlap_min=overlap.min,
                        overlap_max=overlap.max,
                    )
                )
