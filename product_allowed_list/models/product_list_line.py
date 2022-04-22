# Copyright 2021 Camptocamp SA
# @author: Julien Coux <julien.coux@camptocamp.com>
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductListLine(models.Model):
    _name = "product.allowed.list.line"
    _description = "Product allowed list configuration Line"

    product_list_id = fields.Many2one(
        string="Product list configuration",
        comodel_name="product.allowed.list",
        required=True,
    )
    product_template_id = fields.Many2one(
        comodel_name="product.template",
        domain=[("sale_ok", "=", True)],
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        domain="[('product_tmpl_id', '=', product_template_id)]",
    )
    display_name = fields.Char(compute="_compute_display_name")

    def find_for_product(self, prod, config=None):
        domain = [
            "|",
            ("product_id", "=", prod.id),
            "&",
            ("product_id", "=", False),
            ("product_template_id", "=", prod.product_tmpl_id.id),
        ]
        if config:
            domain.append(("product_list_id", "=", config.id))
        return self.search(domain)

    @api.depends("product_list_id", "product_template_id", "product_id")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = rec._name_get()

    def _name_get(self):
        parts = [
            f"[{self.product_list_id.display_name}]",
            self.product_id.display_name or self.product_template_id.display_name,
            f"({self.id})",
        ]
        return " ".join(parts)
