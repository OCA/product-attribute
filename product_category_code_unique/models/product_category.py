# Copyright 2021 ACSONE SA/NV
# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):

    _inherit = "product.category"

    def _get_parents(self):
        self.ensure_one()
        return self.search([("parent_id", "parent_of", self.id)])

    def _get_children(self):
        self.ensure_one()
        return self.search([("parent_id", "child_of", self.id)])

    def _get_hierarchy_categories_for_code_unique(self):
        self.ensure_one()
        return self._get_parents() + self._get_children()

    def _code_restriction(self, restriction=False):
        restriction = restriction or self.env["ir.config_parameter"].get_param(
            "product_code_unique.product_code_unique_restriction", False
        )
        if restriction in ["system", "direct", "hierarchy"]:
            codes_to_check = self.read_group(
                domain=[("code", "!=", False)], fields=["code"], groupby=["code"]
            )
            codes_to_check = list(
                filter(lambda code: code["code_count"] > 1, codes_to_check)
            )
            if codes_to_check:
                if restriction == "system":
                    raise ValidationError(
                        _("The category code must be unique within the system!")
                    )
                codes = [code["code"] for code in codes_to_check]
                cats_to_check = self.search([("code", "in", codes)])
                if restriction == "direct" and cats_to_check.filtered(
                    lambda cat: cat.parent_id.code == cat.code
                ):
                    raise ValidationError(
                        _(
                            "The category code must be unique within parent and children!"
                        )
                    )
                elif restriction == "hierarchy":
                    for cat in cats_to_check:
                        to_check = cat._get_hierarchy_categories_for_code_unique()
                        domain = [("code", "=", cat.code), ("id", "in", to_check.ids)]
                        if self.search_count(domain) > 1:
                            raise ValidationError(
                                _(
                                    "The category code must be unique within category "
                                    "hierarchy!"
                                )
                            )

    @api.constrains("code", "parent_id", "child_id")
    def _check_code(self):
        self._code_restriction()

    @api.model
    def _get_next_code(self):
        return self.env["ir.sequence"].next_by_code("product.category")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "code" not in vals or vals["code"] == "/":
                vals["code"] = self._get_next_code()
        return super().create(vals_list)

    def write(self, vals):
        for category in self:
            value = vals.copy()
            code = value.setdefault("code", category.code)
            if code in [False, "/"]:
                value["code"] = self._get_next_code()
            super(ProductCategory, category).write(value)
        return True
