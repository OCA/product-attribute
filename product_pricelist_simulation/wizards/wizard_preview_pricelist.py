# Copyright 2022 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class PricelistSimulation(models.TransientModel):
    _name = "wizard.preview.pricelist"
    _description = "wizard - Preview Pricelist"

    @api.model
    def default_get(self, fields):
        vals = super().default_get(fields)
        if self.env.context.get("active_model") == "product.template":
            vals["template_id"] = self.env.context.get("active_id")
        else:
            active_id = self.env.context.get("active_id")
            product = self.env["product.product"].browse(active_id)
            vals["product_id"] = product.id
            vals["template_id"] = product.product_tmpl_id.id
        return vals

    template_id = fields.Many2one(
        comodel_name="product.template", string="Product Template", readonly=True
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        domain="[('product_tmpl_id', '=', template_id)]",
        string="Product Variant",
    )
    product_qty = fields.Float(string="Quantity", default=1, required=True)
    price_date = fields.Date(
        string="Date", default=fields.Date.context_today, required=True
    )
    line_ids = fields.One2many(
        string="Simulation Lines",
        comodel_name="wizard.preview.pricelist.line",
        inverse_name="simulation_id",
        compute="_compute_line_ids",
    )
    variant_count = fields.Integer(
        string="Variants Count", compute="_compute_variant_count"
    )

    @api.depends("template_id", "product_id", "product_qty", "price_date")
    def _compute_line_ids(self):
        self.ensure_one()
        pricelists = self.env["product.pricelist"].search(
            [("show_in_simulation", "=", True)],
        )
        line_ids_vals = []
        for variant in self.product_id or self.template_id.product_variant_ids:
            for pricelist in pricelists:
                vals = self._prepare_simulation_lines_vals(variant, pricelist)
                line_ids_vals.append((0, False, vals))
        self.line_ids = line_ids_vals

    def _prepare_simulation_lines_vals(self, variant, pricelist):
        price = variant.with_context(
            pricelist=pricelist.id, quantity=self.product_qty, date=self.price_date,
        ).price
        return {
            "product_id": variant.id,
            "pricelist_id": pricelist.id,
            "price": price,
        }

    @api.depends("template_id")
    def _compute_variant_count(self):
        self.ensure_one()
        self.variant_count = 1
        if not self.product_id:
            self.variant_count = len(self.template_id.product_variant_ids)


class PricelistSimulationLine(models.TransientModel):
    _name = "wizard.preview.pricelist.line"
    _description = "wizard - Preview Pricelist Line"

    simulation_id = fields.Many2one(
        string="Simulation", comodel_name="wizard.preview.pricelist",
    )
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product Variant", readonly=True,
    )
    pricelist_id = fields.Many2one(
        comodel_name="product.pricelist", string="Pricelist", readonly=True,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        related="pricelist_id.currency_id",
        string="Currency",
        readonly=True,
    )
    price = fields.Monetary(
        string="Price", digits="Price", readonly=True, currency_field="currency_id"
    )
