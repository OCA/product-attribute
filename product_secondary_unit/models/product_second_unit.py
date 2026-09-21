# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.tools.float_utils import float_round


class ProductSecondaryUnit(models.Model):
    _name = "product.secondary.unit"
    _description = "Product Secondary Unit"
    _rec_names_search = ["name", "code"]

    name = fields.Char(required=True, translate=True)
    code = fields.Char()
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        string="Product Template",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product Variant",
        ondelete="cascade",
    )
    uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Secondary Unit of Measure",
        required=True,
        help="Default Secondary Unit of Measure.",
    )
    dependency_type = fields.Selection(
        selection=[
            ("dependent", "Dependent"),
            ("independent", "Independent"),
            ("secondary_priority", "Secondary unit priority"),
        ],
        default="dependent",
        help="If dependency type is 'dependent' the factor is used to "
        "compute quantity in primary unit and vice versa. "
        "If 'independent', primary and secondary unit are unrelated - "
        "for example if you sell a service by package (1 unit) and want "
        "to put the real time (e.g. 4 hours) to allow employee scheduling. "
        "If 'secondary unit priority', the factor is only used to "
        "estimate the primary unit from the secondary one (like "
        "'dependent'), but the secondary unit is never itself recomputed "
        "back from the primary one (like 'independent') - for example "
        "counting pieces of a product sold by weight, where the real "
        "weight of each piece varies but the piece count must stay exact.",
    )
    factor = fields.Float(string="Secondary Unit Factor", default=1.0, required=True)
    active = fields.Boolean(default=True)

    @api.depends("name", "factor")
    def _compute_display_name(self):
        for unit in self:
            unit.display_name = f"{unit.name}-{unit.factor}"

    def _get_secondary_qty(self, qty, uom, product_uom_field="uom_id"):
        """Helper method to obtain the secondary uom quantity from a given main unit"""
        self.ensure_one()
        uom_product = (
            self.product_id[product_uom_field]
            or self.product_tmpl_id[product_uom_field]
        )
        if uom != uom_product:
            qty = uom._compute_quantity(qty, uom_product)
        return float_round(
            qty / (self.factor or 1.0), precision_rounding=self.uom_id.rounding
        )
