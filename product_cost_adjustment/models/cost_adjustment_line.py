# Copyright 2021 - Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class CostAdjustmentLine(models.Model):
    _name = "cost.adjustment.line"
    _description = "Cost Adjustment Line"
    _order = "product_id, cost_adjustment_id"

    def _get_qty(self):
        for line in self:
            if line.state not in ("posted"):
                line.qty_on_hand = line.product_id.sudo().quantity_svl

    is_editable = fields.Boolean(
        string="Editable?", help="Technical field to restrict editing."
    )
    cost_adjustment_id = fields.Many2one(
        "cost.adjustment",
        string="Cost Adjustment",
        check_company=True,
        index=True,
        ondelete="cascade",
        required=True,
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        check_company=True,
        domain="""[
            ('type', '=', 'product'),
             '|', ('company_id', '=', False),
             ('company_id', '=', company_id)
            ]""",
        index=True,
        required=True,
    )
    product_original_cost = fields.Float(
        string="Original Cost",
        readonly=True,
        default=0,
        copy=False,
    )
    product_cost = fields.Float(
        string="New Cost",
        readonly=True,
        states={"confirm": [("readonly", False)]},
        default=0,
        copy=False,
    )
    difference_cost = fields.Float(
        string="Difference",
        compute="_compute_difference",
        help="Indicates the gap between the product's original cost and its new cost.",
        readonly=True,
        search="_search_difference_cost",
    )
    categ_id = fields.Many2one(related="product_id.categ_id", store=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        related="cost_adjustment_id.company_id",
        index=True,
        readonly=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        related="company_id.currency_id",
    )
    state = fields.Selection(string="Status", related="cost_adjustment_id.state")
    cost_adjustment_date = fields.Datetime(
        string="Cost Adjustment Date",
        related="cost_adjustment_id.date",
        help="Last date at which the On Hand Quantity has been computed.",
    )
    qty_on_hand = fields.Float(string="QTY on Hand", readonly=True)
    total_difference = fields.Float(
        string="Total Difference",
        compute="_compute_difference",
        store=True,
    )
    price_outdated = fields.Boolean(
        string="Price Outdated", compute="_compute_outdated"
    )
    qty_outdated = fields.Boolean(string="Qty Outdated", compute="_compute_outdated")

    @api.depends("product_cost", "product_original_cost", "qty_on_hand")
    def _compute_difference(self):
        for line in self:
            cost_diff = line.product_cost - line.product_original_cost
            line.difference_cost = cost_diff
            line.total_difference = cost_diff * line.qty_on_hand

    @api.depends(
        "product_original_cost", "product_id.standard_price", "product_id.quantity_svl"
    )
    def _compute_outdated(self):
        for line in self:
            line.price_outdated = (
                True
                if line.product_original_cost != line.product_id.standard_price
                else False
            )
            line.qty_outdated = (
                True
                if line.product_id.sudo().quantity_svl != line.qty_on_hand
                else False
            )

    @api.onchange("product_id")
    def _set_costs(self):
        for line in self:
            if line.state not in ("posted"):
                self.product_cost = self.product_id.standard_price
                self.product_original_cost = self.product_id.standard_price
                self.qty_on_hand = line.product_id.sudo().quantity_svl

    def action_refresh_quantity(self):
        filtered_lines = self.filtered(lambda l: l.state != "posted")
        for line in filtered_lines:
            quantity = line.product_id.sudo().quantity_svl
            if line.qty_on_hand != quantity:
                line.qty_on_hand = quantity
                # line.outdated = False

    def action_get_origin_cost(self):
        filtered_lines = self.filtered(lambda l: l.state != "posted")
        for line in filtered_lines:
            origin_cost = line.product_id.standard_price
            if line.product_original_cost != origin_cost:
                line.product_original_cost = origin_cost

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._check_no_duplicate_line()
        res.action_refresh_quantity()
        return res

    def write(self, vals):
        res = super().write(vals)
        self._check_no_duplicate_line()
        return res

    def _check_no_duplicate_line(self):
        for line in self:
            domain = [
                ("id", "!=", line.id),
                ("product_id", "=", line.product_id.id),
                ("cost_adjustment_id", "=", line.cost_adjustment_id.id),
            ]
            existings = self.search_count(domain)
            if existings:
                raise UserError(
                    _(
                        """There is already one cost adjustment line for this product,
                         you should rather modify this one instead of creating a
                         new one."""
                    )
                )

    def _search_difference_cost(self, operator, value):
        if operator == "=":
            result = True
        elif operator == "!=":
            result = False
        else:
            raise NotImplementedError()
        lines = self.search(
            [
                (
                    "cost_adjustment_id",
                    "=",
                    self.env.context.get("default_cost_adjustment_id"),
                )
            ]
        )
        line_ids = lines.filtered(
            lambda line: float_is_zero(
                line.difference_cost, line.product_id.uom_id.rounding
            )
            == result
        ).ids
        return [("id", "in", line_ids)]
