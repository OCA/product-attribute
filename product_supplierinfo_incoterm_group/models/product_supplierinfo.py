# Copyright 2026 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Kévin Roche <kevin.roche@akretion.com>

from odoo import fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    incoterm_id = fields.Many2one(
        related="group_id.incoterm_id", store=True, readonly=False
    )

    def _fields_for_group_match(self):
        mapping = dict(super()._fields_for_group_match())
        mapping["incoterm_id"] = "incoterm_id"
        return mapping

    def _get_or_create_group(self, vals):
        if "incoterm_id" not in vals and vals.get("partner_id"):
            partner = self.env["res.partner"].browse(vals["partner_id"])
            vals = dict(vals, incoterm_id=partner.purchase_incoterm_id.id)
        return super()._get_or_create_group(vals)
