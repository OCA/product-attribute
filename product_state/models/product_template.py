# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields


class ProductState(models.Model):
    _name = "product.state"
    _description = "Product State"
    _order = "sequence, id"

    name = fields.Char("State Name", required=True, translate=True)
    code = fields.Char("State Code", required=True)
    sequence = fields.Integer("Sequence", help="Used to order the States", default=25)
    description = fields.Text(translate=True)
    product_ids = fields.One2many(
        "product.template", "product_state_id", string="State Products",
    )
    products_count = fields.Integer(
        string="Number of products", compute="_compute_products_count",
    )

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


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    state = fields.Char(
        string="Product Status",
        index=True,
        compute="_compute_product_state",
        inverse="_inverse_product_state",
        store=True,
    )
    product_state_id = fields.Many2one(
        comodel_name="product.state",
        string="State",
        help="Select a state for this product",
    )

    @api.depends("product_state_id")
    def _compute_product_state(self):
        for product_tmpl in self:
            product_tmpl.state = product_tmpl.product_state_id.code

    def _inverse_product_state(self):
        ProductState = self.env["product.state"]
        for product_tmpl in self:
            product_state = ProductState.search(
                [("code", "=", product_tmpl.state)], limit=1
            )
            if product_tmpl.state and not product_state:
                product_state = ProductState.create({"name": product_tmpl.state})
            product_tmpl.product_state_id = product_state.id
