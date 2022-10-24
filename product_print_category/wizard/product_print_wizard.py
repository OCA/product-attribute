# Copyright (C) 2012-Today GRAP (http://www.grap.coop)
# @author Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPrintWizard(models.TransientModel):
    _name = "product.print.wizard"
    _description = "Wizard for printing products"

    line_ids = fields.One2many(
        comodel_name="product.print.wizard.line",
        inverse_name="wizard_id",
        string="Lines",
        default=lambda s: s._default_line_ids(),
    )

    @api.model
    def _default_line_ids(self):
        lines_vals = []
        context = self.env.context
        ProductProduct = self.env["product.product"]
        if context.get("active_model", False) == "product.print.category":
            domain = [
                ("print_category_id.id", "in", context.get("active_ids", [])),
            ]
            if not context.get("all_products", False):
                domain.append(("to_print", "=", True))
            products = ProductProduct.search(domain)

        elif context.get("active_model", False) == "product.product":
            product_ids = context.get("active_ids", [])
            products = ProductProduct.browse(product_ids)
        elif context.get("active_model", False) == "product.template":
            template_ids = context.get("active_ids", [])
            products = ProductProduct.search([("product_tmpl_id", "in", template_ids)])
        else:
            return False

        for product in products:
            lines_vals.append(
                (
                    0,
                    0,
                    {
                        "product_id": product.id,
                        "print_category_id": product.print_category_id.id,
                        "quantity": 1,
                    },
                )
            )
        return lines_vals

    def print_report(self):
        self.ensure_one()
        lines_without_category = self.mapped("line_ids").filtered(
            lambda x: not x.print_category_id
        )
        if lines_without_category:
            raise ValidationError(
                _("Please set a print category for the following lines \n\n- %s")
                % ("\n- ".join(lines_without_category.mapped("product_id.name")))
            )
        self._prepare_data()
        return self.env.ref("product_print_category.pricetag").report_action(
            self.line_ids
        )

    def _prepare_data(self):
        self.ensure_one()
        return {
            "line_data": [x.id for x in self.line_ids],
        }

    def _prepare_product_data(self):
        self.ensure_one()
        product_data = {}
        for line in self.line_ids:
            if line.product_id.id not in product_data:
                product_data[line.product_id.id] = line.quantity
            else:
                product_data[line.product_id.id] += line.quantity
        return product_data
