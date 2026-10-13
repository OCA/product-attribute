# Copyright (C) 2026 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    incoterm_id = fields.Many2one(
        comodel_name="account.incoterms",
        string="Incoterm",
        ondelete="restrict",
        compute="_compute_incoterm_id",
        store=True,
        readonly=False,
    )

    @api.depends("partner_id.purchase_incoterm_id")
    def _compute_incoterm_id(self):
        for rec in self:
            rec.incoterm_id = rec.partner_id.purchase_incoterm_id
