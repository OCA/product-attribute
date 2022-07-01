# Copyright 2022 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class PricelistSimulation(models.TransientModel):
    _name = "pricelist.simulation"
    _description = "Pricelist Simulation"

    @api.model
    def default_get(self, fields):
        vals = super().default_get(fields)
        action_model = self.env.context.get("active_model")
        active_id = self.env.context.get("active_id")
        model = self.env[action_model].browse(active_id)
        variants = model if model.is_product_variant else model.product_variant_ids
        pricelists = self.env["product.pricelist"].search(
            [("show_in_simulation", "=", True)],
        )
        line_ids_vals = []
        for variant in variants:
            for pricelist in pricelists:
                price = variant.with_context(pricelist=pricelist.id).price
                line_ids_vals.append(
                    (
                        0,
                        False,
                        {
                            "product_id": variant.id,
                            "pricelist_id": pricelist.id,
                            "price": price,
                        },
                    )
                )
        vals["line_ids"] = line_ids_vals
        vals["variant_count"] = len(variants)
        return vals

    line_ids = fields.One2many(
        string="line",
        comodel_name="pricelist.simulation.line",
        inverse_name="simulation_id",
    )
    variant_count = fields.Integer(string="Variants")


class PricelistSimulationLine(models.TransientModel):
    _name = "pricelist.simulation.line"
    _description = "Pricelist Simulation Line"

    simulation_id = fields.Many2one(
        string="Simulation", comodel_name="pricelist.simulation",
    )
    product_id = fields.Many2one(
        comodel_name="product.product", string="Product variant", readonly=True,
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
    price = fields.Monetary(string="Price Simulated", digits="Price", readonly=True,)
