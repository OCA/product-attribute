# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv.expression import FALSE_DOMAIN
from odoo.tools.float_utils import float_is_zero, float_round


class ProductSupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    packaging_id = fields.Many2one(
        comodel_name="product.packaging",
        ondelete="restrict",
    )
    packaging_qty = fields.Float(
        compute="_compute_packaging_qty",
    )
    packaging_id_domain = fields.Binary(compute="_compute_packaging_id_domain")
    packaging_min_qty = fields.Float(
        compute="_compute_packaging_min_qty",
        inverse="_inverse_packaging_min_qty",
        string="Packaging Min. Quantity",
        default=0.0,
        digits="Product Unit of Measure",
        store=True,
        readonly=False,
    )
    packaging_price = fields.Float(
        compute="_compute_packaging_price",
        inverse="_inverse_packaging_price",
        default=0.0,
        digits="Product Price",
        store=True,
        readonly=False,
    )

    @api.depends("packaging_id.qty")
    def _compute_packaging_qty(self):
        for rec in self:
            rec.packaging_qty = rec.packaging_id.qty

    @api.depends(
        "product_id",
        "product_tmpl_id",
    )
    def _compute_packaging_id_domain(self):
        for rec in self:
            product = rec.product_id
            tmpl = rec.product_tmpl_id
            domain = [
                ("purchase", "=", True),
                "|",
                ("company_id", "=", rec.company_id.id),
                ("company_id", "=", False),
            ]
            if product:
                domain.append(("product_id", "=", product.id))
            elif tmpl:
                domain.append(
                    ("product_id.product_tmpl_id", "=", rec.product_tmpl_id.id)
                )
            else:
                domain = FALSE_DOMAIN
            rec.packaging_id_domain = domain

    @api.depends("packaging_id", "product_uom", "min_qty")
    def _compute_packaging_min_qty(self):
        for rec in self:
            packaging = rec.packaging_id
            packaging_qty = 0.0
            if packaging:
                packaging_uom = packaging.product_uom_id
                packaging_uom_qty = rec.product_uom._compute_quantity(
                    rec.min_qty, packaging_uom
                )
                packaging_qty = float_round(
                    packaging_uom_qty / packaging.qty,
                    precision_rounding=packaging_uom.rounding,
                )
            rec.packaging_min_qty = packaging_qty

    @api.depends(
        "price",
        "packaging_id",
        "packaging_qty",
    )
    def _compute_packaging_price(self):
        price_digits = self.env["decimal.precision"].precision_get("Product Price")
        qty_digits = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        for rec in self:
            price = 0
            packaging_qty = rec.packaging_qty
            if not float_is_zero(packaging_qty, precision_digits=qty_digits):
                price = float_round(
                    rec.price * packaging_qty,
                    precision_digits=price_digits,
                )
            rec.packaging_price = price

    @api.constrains(
        "packaging_id",
        "product_id",
    )
    def _check_packaging_id(self):
        for rec in self:
            packaging = rec.packaging_id
            if not packaging:
                continue
            product = rec.product_id
            pack_product = packaging.product_id
            tmpl = rec.product_tmpl_id
            is_valid = (
                product == packaging.product_id
                if product
                else pack_product.product_tmpl_id == tmpl
            )
            if not is_valid:
                raise ValidationError(
                    _(
                        "Selected packaging (%(packaging)s) is not "
                        "linked to current product %(product)s",
                        packaging=rec.display_name,
                        product=tmpl.display_name,
                    )
                )

    @api.onchange("packaging_min_qty")
    def _inverse_packaging_min_qty(self):
        for rec in self:
            packaging = rec.packaging_id
            if not packaging:
                continue
            packaging_uom = packaging.product_uom_id
            uom = rec.product_uom or rec.product_tmpl_id.uom_id
            packaging_uom_qty = packaging_uom._compute_quantity(
                rec.packaging_min_qty, uom
            )
            packaging_qty = float_round(
                packaging_uom_qty * packaging.qty,
                precision_rounding=packaging_uom.rounding,
            )
            rec.min_qty = packaging_qty

    @api.onchange("packaging_price", "packaging_qty")
    def _inverse_packaging_price(self):
        price_digits = self.env["decimal.precision"].precision_get("Product Price")
        qty_digits = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        for rec in self:
            packaging_qty = rec.packaging_qty or rec.packaging_id.qty
            packaging_price = rec.packaging_price
            skip = float_is_zero(
                packaging_price, precision_digits=price_digits
            ) or float_is_zero(packaging_qty, precision_digits=qty_digits)
            if skip:
                continue
            rec.price = float_round(
                packaging_price / packaging_qty, precision_digits=price_digits
            )
