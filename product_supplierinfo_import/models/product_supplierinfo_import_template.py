# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductSupplierInfoImportTemplate(models.Model):
    _name = "product.supplierinfo.import.template"
    _description = "Templates to be detected when importing vendor pricelist"

    name = fields.Char(required=True)
    header_offset = fields.Integer(required=True, default=0)
    barcode_header_name = fields.Char(required=True)
    template_line_ids = fields.One2many(
        comodel_name="product.supplierinfo.import.template.line",
        inverse_name="template_id",
        string="Headers mapping",
    )

    def _template_headers(self):
        self.ensure_one()
        # Trim left and right chars and always convert new lines into spaces to avoid
        # copy/paste discrepancies
        return set(
            [
                h.replace("\n", " ").strip()
                for h in self.template_line_ids.mapped("header_name")
            ]
            + [self.barcode_header_name]
        )


class ProductSupplierInfoImportTemplateLine(models.Model):
    _name = "product.supplierinfo.import.template.line"
    _description = "Vendor import columns and fields"

    template_id = fields.Many2one(comodel_name="product.supplierinfo.import.template")
    header_name = fields.Text(
        help="Copy it directly from the origin cell so it matches right"
    )
    field_id = fields.Many2one(
        comodel_name="ir.model.fields", domain=[("model", "=", "product.supplierinfo")]
    )
