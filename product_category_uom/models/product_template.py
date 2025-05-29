# Copyright 2025 ForgeFlow (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import defaultdict

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.onchange("categ_id")
    def _onchange_categ_id_set_uom(self):
        if self.categ_id and self.categ_id.uom_id:
            self.uom_id = self.categ_id.uom_id

    def set_uom_from_category(self):
        records_by_categ = defaultdict(lambda: self.browse())
        for rec in self:
            records_by_categ[rec.categ_id] += rec
        for categ, records in records_by_categ.items():
            if not categ.uom_id:
                continue
            records.write({"uom_id": categ.uom_id.id})
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("categ_id") and "uom_id" not in vals:
                categ = self.env["product.category"].browse(vals["categ_id"])
                if categ.uom_id:
                    vals["uom_id"] = categ.uom_id.id
        return super().create(vals_list)
