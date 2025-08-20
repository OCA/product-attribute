# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    default_code_ids = fields.One2many(
        "product.default_code", "product_id", string="Internal References"
    )

    default_code = fields.Char(
        string="Internal Reference",
        compute="_compute_default_code",
        store=True,
        inverse="_inverse_default_code",
        compute_sudo=True,
    )

    @api.depends("default_code_ids.name", "default_code_ids.sequence")
    def _compute_default_code(self):
        for product in self:
            product.default_code = product.default_code_ids[:1].name

    def _inverse_default_code(self):
        codes_to_unlink = self.env["product.default_code"]
        create_code_vals_list = []
        for product in self:
            if product.default_code_ids and product.default_code:
                product.default_code_ids[0].name = product.default_code
            elif not product.default_code:
                codes_to_unlink |= product.default_code_ids
            else:
                create_code_vals_list.append(product._prepare_default_code_vals())
        if codes_to_unlink:
            codes_to_unlink.unlink()
        if create_code_vals_list:
            self.env["product.default_code"].create(create_code_vals_list)

    def _prepare_default_code_vals(self):
        self.ensure_one()
        return {
            "product_id": self.id,
            "name": self.default_code,
        }

    @api.model
    def _search(self, domain, *args, **kwargs):
        for sub_domain in list(filter(lambda x: x[0] == "default_code", domain)):
            domain = self._get_default_code_domain(sub_domain, domain)
        return super()._search(domain, *args, **kwargs)

    def _get_default_code_domain(self, sub_domain, domain):
        operator = sub_domain[1]
        value = sub_domain[2]
        codes = self.env["product.default_code"].search([("name", operator, value)])
        domain = [
            ("default_code_ids", "in", codes.ids)
            if x[0] == "default_code" and x[2] == value
            else x
            for x in domain
        ]
        return domain
