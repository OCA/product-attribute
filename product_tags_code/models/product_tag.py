# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTag(models.Model):
    _inherit = "product.tag"

    code = fields.Char(
        compute="_compute_code",
        readonly=False,
        inverse="_inverse_code",
        store=True,
    )

    _sql_constraints = [
        (
            "code_uniq",
            "unique(code)",
            "Product template tag code already exists",
        )
    ]

    @api.depends("name", "code")
    def _compute_code(self):
        for rec in self:
            if rec.name and rec.name.strip():
                rec.code = self.env["ir.http"]._slugify(rec.name)
            else:
                rec.code = ""

    def _inverse_code(self):
        for rec in self:
            rec.code = self.env["ir.http"]._slugify(rec.code)
