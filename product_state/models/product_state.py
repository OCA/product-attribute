# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductState(models.Model):
    _name = "product.state"
    _description = "Product State"
    _order = "sequence, id"

    name = fields.Char(comodel_name="State Name", required=True, translate=True)
    code = fields.Char(string="State Code", required=True)
    sequence = fields.Integer(
        string="Sequence", help="Used to order the States", default=25
    )
    active = fields.Boolean(default=True)
    description = fields.Text(translate=True)
    product_ids = fields.One2many(
        comodel_name="product.template",
        inverse_name="product_state_id",
        string="State Products",
    )
    products_count = fields.Integer(
        string="Number of products",
        compute="_compute_products_count",
    )
    default = fields.Boolean("Default state")
    _sql_constraints = [
        ("code_unique", "UNIQUE(code)", "Product State Code must be unique.")
    ]

    @api.depends("product_ids")
    def _compute_products_count(self):
        data = self.env["product.template"].read_group(
            [("product_state_id", "in", self.ids)],
            ["product_state_id"],
            ["product_state_id"],
        )
        mapped_data = {
            record["product_state_id"][0]: record["product_state_id_count"]
            for record in data
        }
        for state in self:
            state.products_count = mapped_data.get(state.id, 0)

    @api.constrains("default")
    def _check_default(self):
        if self.search_count([("default", "=", True)]) > 1:
            raise ValidationError(_("There should be only one default state"))
