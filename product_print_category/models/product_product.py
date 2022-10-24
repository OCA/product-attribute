# Copyright (C) 2016-Today: La Louve (<http://www.lalouve.net/>)
# Copyright (C) 2022-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "product.print.category.mixin"]

    # Columns Section
    print_category_id = fields.Many2one(
        string="Print Category",
        comodel_name="product.print.category",
        default=lambda s: s._default_print_category_id(),
    )

    to_print = fields.Boolean()

    # Default Section
    def _default_print_category_id(self):
        return self.env.user.company_id.print_category_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("print_category_id", False):
                vals["to_print"] = True
        return super().create(vals)

    def write(self, vals):
        res = super(
            ProductProduct, self.with_context(update_to_print_category=False)
        ).write(vals)
        self._update_to_print_values(vals)
        return res
