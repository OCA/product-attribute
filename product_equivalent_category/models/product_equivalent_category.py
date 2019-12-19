# Copyright 2019 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductEquivalentCategory(models.Model):
    _name = "product.equivalent.category"
    _description = "Product Equivalent Category"

    name = fields.Char("Name", index=True, required=True, translate=True)
    description = fields.Text("Description")
    product_count = fields.Integer(
        "# Products",
        compute="_compute_product_count",
        help="The number of products under this category",
    )

    @api.multi
    def _compute_product_count(self):
        categ_data = self.env["product.template"].read_group([
            ('equivalent_categ_id', 'in', self.ids),
        ], ['equivalent_categ_id'], ['equivalent_categ_id'])
        mapped_data = {
            record['equivalent_categ_id'][0]: record[
                'equivalent_categ_id_count']
            for record in categ_data
        }
        for categ in self:
            categ.product_count = mapped_data.get(categ.id, 0)

    @api.multi
    def action_view_product_template_ids(self):
        self.ensure_one()
        action = self.env.ref('product.product_template_action_all')
        result = action.read()[0]
        result['domain'] = [("equivalent_categ_id", "=", self.id)]
        result['context'] = {}
        return result
