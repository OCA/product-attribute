#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import float_compare


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="uom.uom",
    )
    uom_min_quantity = fields.Float(
        string="Min. Quantity in UoM",
        digits="Product Unit of Measure",
    )

    @api.onchange(
        "product_id",
        "product_tmpl_id",
    )
    def onchange_product_uom(self):
        product = self.product_id or self.product_tmpl_id
        product_uom = product.uom_id
        if self.uom_id != product_uom:
            self.uom_id = product_uom

    def _sync_uom_min_quantity(
        self, source_quantity, source_uom, target_uom, target_qty_field
    ):
        """Convert `source_quantity` (in `source_uom`) to `target_uom`.
        Assign the result to field `self.target_qty_field`, if different."""
        self.ensure_one()
        if target_uom != source_uom:
            expected_target_quantity = source_uom._compute_quantity(
                source_quantity,
                target_uom,
                raise_if_failure=False,
                round=False,
            )
        else:
            expected_target_quantity = source_quantity

        # Assign only if different,
        # according to the precision of target field
        all_digits, precision_digits = self.fields_get(
            allfields=[
                target_qty_field,
            ],
            attributes=[
                "digits",
            ],
        )[target_qty_field]["digits"]
        if float_compare(
            self[target_qty_field],
            expected_target_quantity,
            precision_digits=precision_digits,
        ):
            self[target_qty_field] = expected_target_quantity

    @api.onchange(
        "product_id",
        "product_tmpl_id",
        "uom_id",
        "uom_min_quantity",
    )
    def onchange_uom_min_quantity(self):
        product = self.product_id or self.product_tmpl_id
        product_uom = product.uom_id
        self._sync_uom_min_quantity(
            self.uom_min_quantity,
            self.uom_id,
            product_uom,
            "min_quantity",
        )

    @api.onchange(
        "product_id",
        "product_tmpl_id",
        "min_quantity",
    )
    def onchange_min_quantity(self):
        product = self.product_id or self.product_tmpl_id
        product_uom = product.uom_id
        self._sync_uom_min_quantity(
            self.min_quantity,
            product_uom,
            self.uom_id,
            "uom_min_quantity",
        )
