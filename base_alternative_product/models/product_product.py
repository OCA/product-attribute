# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    alternative_product_ids = fields.Many2many(
        string="Alternative Products",
        comodel_name="product.product",
        relation="product_alternatives_rel",
        column1="product_id",
        column2="alternative_id",
    )

    def _manage_related_products(self, related_products_command):
        if self.env.company.symetrical_alternative_products:
            prod2link = []
            link_code = 4
            prod2unlink = []
            unlink_code = 3
            for command in related_products_command:
                if command[0] == link_code:
                    prod2link.append(command[1])
                elif command[0] == unlink_code:
                    prod2unlink.append(command[1])
                else:
                    raise NotImplementedError(
                        _(
                            "The {} command was detected on updating product alternatives, "
                            "but it is not supported."
                        )
                    )
            if prod2link:
                self.browse(prod2link).exists().with_context(
                    stop_prod_alt_recursion=True
                ).write(
                    {"alternative_product_ids": [(link_code, rec.id) for rec in self]}
                )
            if prod2unlink:
                self.browse(prod2unlink).exists().with_context(
                    stop_prod_alt_recursion=True
                ).write(
                    {"alternative_product_ids": [(unlink_code, rec.id) for rec in self]}
                )

    @api.model_create_multi
    def create(self, vals_list):
        recs = super().create(vals_list)
        for rec, vals in zip(recs, vals_list, strict=False):
            if "alternative_product_ids" in vals:
                rec._manage_related_products(vals["alternative_product_ids"])
        return recs

    def write(self, vals):
        res = super().write(vals)
        if "alternative_product_ids" in vals and not self.env.context.get(
            "stop_prod_alt_recursion"
        ):
            self._manage_related_products(vals["alternative_product_ids"])
        return res
