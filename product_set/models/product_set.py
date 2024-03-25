# Copyright 2015 Anybox S.A.S
# Copyright 2016-2018 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProductSet(models.Model):
    _name = "product.set"
    _description = "Product set"

    name = fields.Char(help="Product set name", required=True, translate=True)
    active = fields.Boolean(default=True)
    ref = fields.Char(
        string="Internal Reference", help="Product set internal reference", copy=False
    )
    set_line_ids = fields.One2many(
        "product.set.line", "product_set_id", string="Products", copy=True
    )
    company_id = fields.Many2one(
        "res.company",
        "Company",
        default=lambda self: self.env.company,
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        required=False,
        ondelete="cascade",
        index=True,
        help="You can attache the set to a specific partner "
        "or no one. If you don't specify one, "
        "it's going to be available for all of them.",
    )

    display_name = fields.Char(
        compute="_compute_display_name",
        string="Display Name",
    )

    @api.depends("name", "ref", "partner_id.name")
    def _compute_display_name(self):
        for rec in self:
            parts = []
            if rec.ref:
                parts.append("[%s]" % rec.ref)
            parts.append(rec.name or "")
            if rec.partner_id and rec.partner_id.name:
                parts.append("@ %s" % rec.partner_id.name)
            rec.display_name = " ".join(map(str, parts))
