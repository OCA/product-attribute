# Copyright (C) 2023-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductPrintCategoryRule(models.Model):
    _name = "product.print.category.rule"
    _description = "Print Category Rules for Product"
    _order = "sequence"

    sequence = fields.Integer(string="Priority", required=True)

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        index=True,
        default=lambda x: x._default_company_id(),
        help="Restrict the access of this rule to the given company",
    )

    main_category_id = fields.Many2one(
        string="Main Category",
        comodel_name="product.category",
        help="This rule will be applied only to products that belong to"
        " the given category, or to its children.",
    )

    print_category_id = fields.Many2one(
        comodel_name="product.print.category",
    )

    def _default_company_id(self):
        return self.env.company

    @api.model
    def get_print_category_rule(self, product):
        # if the required field categ_id is not set
        # we are in a creation process and there is
        # no way to guess the print category at this step.
        if not product.categ_id:
            return False

        return self.search(
            [
                "|",
                ("main_category_id", "parent_of", product.categ_id.id),
                ("main_category_id", "=", False),
            ],
            limit=1,
        )
