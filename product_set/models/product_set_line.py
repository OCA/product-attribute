# Copyright 2015 Anybox S.A.S
# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


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
    product_uom_id = fields.Many2one(
        "product.uom", domain="[('product_id', '=', product_id)]"
    )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        """On product change, set the product_uom_id to the default UoM of the
        new product."""
        for line in self:
            if not line.product_id:
                line.product_uom_id = False

    @api.depends("product_set_id.active")
    def _compute_active(self):
        """Compute the active field based on the product_set_id by default."""
        for line in self:
            if line.product_set_id:
                line.active = line.product_set_id.active
            else:
                line.active = True
