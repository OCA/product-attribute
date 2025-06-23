# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductSupplierInfoImportTemplate(models.Model):
    _name = "product.supplierinfo.import.template"
    _description = "Templates to be detected when importing vendor pricelist"

    name = fields.Char(required=True)
    supplier_id = fields.Many2one(comodel_name="res.partner")
    header_offset = fields.Integer(required=True, default=0)
    sheet_number = fields.Integer(
        required=True,
        default=1,
        help="The number of the sheet page in the spreadsheet where the pricelist are",
    )
    search_header_name = fields.Char(required=True)
    template_line_ids = fields.One2many(
        comodel_name="product.supplierinfo.import.template.line",
        inverse_name="template_id",
        string="Headers mapping",
    )
    only_update_existing = fields.Boolean(
        help="If enabled, only existing supplierinfo records will be updated. "
        "New ones will not be created.",
        default=False,
    )
    show_not_updated_rates = fields.Boolean(
        help="If checked, at the end of the import,"
        " it will display the supplier's rate records that were not updated.",
    )
    import_criteria_field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        domain=[("model", "=", "product.template"), ("ttype", "=", "char")],
        default=lambda self: self.env.ref("product.field_product_template__barcode"),
        help="The field that will be used to match the products"
        "from the excel file with the ones in the Odoo database",
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
            + [self.search_header_name]
        )

    @api.constrains("sheet_number")
    def _check_integer_value(self):
        for record in self:
            if record.sheet_number < 1:
                raise ValidationError(_("The Sheet Number cannot be less than 1."))


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
