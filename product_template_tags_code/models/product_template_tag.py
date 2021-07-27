# Copyright 2020 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.http_routing.models.ir_http import slugify


class ProductTemplateTag(models.Model):

    _inherit = "product.template.tag"

    code = fields.Char(
        string="Code",
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
                rec.code = slugify(rec.name)
            else:
                rec.code = ""

    def _inverse_code(self):
        for rec in self:
            rec.code = slugify(rec.code)
