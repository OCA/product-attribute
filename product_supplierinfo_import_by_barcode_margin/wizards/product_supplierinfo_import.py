# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductSupplierInfoImport(models.TransientModel):
    _inherit = "product.supplierinfo.import"

    sale_margin = fields.Float(required=True)

    def _prepare_supplierinfo_values(self, row_data):
        values = super()._prepare_supplierinfo_values(row_data)
        values["sale_margin"] = self.sale_margin
        return values
