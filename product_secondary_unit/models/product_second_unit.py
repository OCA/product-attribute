# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductSecondaryUnit(models.Model):
    _name = "product.secondary.unit"
    _description = "Product Secondary Unit"

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
        ],
        default="dependent",
        help="If dependency type is 'dependent' the factor is used "
        "to compute quantity in primary unit,"
        "otherwise primary and secondary unit are independent. "
        "For example if you sell service"
        "by package (1 unit for example) and you want to put the "
        "real time (ex : 4 hours) to allows employee scheduling",
    )
    factor = fields.Float(string="Secondary Unit Factor", default=1.0, required=True)
    active = fields.Boolean(default=True)

    def name_get(self):
        result = []
        for unit in self:
            result.append(
                (
                    unit.id,
                    f"{unit.name}-{unit.factor}",
                )
            )
        return result

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        if args is None:
            args = []
        units = self.search([("code", "=", name)] + args, limit=1)
        if not units:
            return super().name_search(
                name=name, args=args, operator=operator, limit=limit
            )
        return units.name_get()
