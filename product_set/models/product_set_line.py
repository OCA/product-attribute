# Copyright 2015 Anybox S.A.S
# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class ProductSetLine(models.Model):
    _name = "product.set.line"
    _description = "Product set line"
    _rec_name = "product_id"
    _order = "product_set_id, sequence, product_id"

    display_type = fields.Selection(
        [
            ("line_section", "Section"),
            ("line_note", "Note"),
        ]
    )

    product_id = fields.Many2one(
        comodel_name="product.product",
        domain=[("sale_ok", "=", True)],
        string="Product",
        required=False,
    )
    quantity = fields.Float(
        digits="Product Unit of Measure", required=True, default=1.0
    )
    product_set_id = fields.Many2one("product.set", string="Set", ondelete="cascade")
    active = fields.Boolean(
        compute="_compute_active",
        readonly=False,
        store=True,
        default=True,
    )
    sequence = fields.Integer(required=True, default=0)
    company_id = fields.Many2one(
        "res.company", related="product_set_id.company_id", store=True, readonly=True
    )
    name = fields.Char()
    product_packaging_id = fields.Many2one(
        "product.packaging", domain="[('product_id', '=', product_id)]"
    )
    product_packaging_qty = fields.Float(
        compute="_compute_product_packaging_qty",
        inverse="_inverse_product_packaging_qty",
        digits="Product Unit of Measure",
    )

    def _compute_active(self):
        """Compute the active field based on the product_set_id by default."""
        for line in self:
            if line.product_set_id:
                line.active = line.product_set_id.active
            else:
                line.active = True

    @api.depends(
        "quantity",
        "product_packaging_id",
        "product_packaging_id.qty",
        "product_id.packaging_ids",
    )
    def _compute_product_packaging_qty(self):
        for line in self:
            uom_rounding = line.product_id.uom_id.rounding
            if not line.product_packaging_id or float_is_zero(
                line.quantity, precision_rounding=uom_rounding
            ):
                line.product_packaging_qty = 0
                continue
            line.product_packaging_qty = line.quantity / line.product_packaging_id.qty
            line.update(line._prepare_product_packaging_qty_values())

    def _inverse_product_packaging_qty(self):
        for line in self:
            if line.product_packaging_qty and not line.product_packaging_id:
                raise UserError(
                    self.env._(
                        "You must define a package before setting a quantity "
                        "of said package."
                    )
                )
            if line.product_packaging_id and line.product_packaging_qty:
                line.write(line._prepare_product_packaging_qty_values())

    def _prepare_product_packaging_qty_values(self):
        self.ensure_one()
        return {
            "quantity": self.product_packaging_id.qty * self.product_packaging_qty,
        }
