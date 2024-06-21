# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64
import logging

import xlrd
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ProductSupplierInfoImport(models.TransientModel):
    _name = "product.supplierinfo.import"
    _description = "Import supplier info records"

    supplier_id = fields.Many2one(comodel_name="res.partner", required=True)
    date_start = fields.Date(string="Validity", required=True)
    delay = fields.Integer()
    create_new_products = fields.Boolean(
        help="If a product isn't found by its barcode, it will be created with the "
        "provided data",
        default=True,
    )
    supplierinfo_file = fields.Binary(required=True)
    supplierinfo_filename = fields.Char()
    template_id = fields.Many2one(comodel_name="product.supplierinfo.import.template")

    @api.model
    def _parse_header(self, header):
        # Trim left and right blank chars and convert newlines for better matching
        return [str(h).replace("\n", " ").strip() for h in header]

    def _detect_template(self, sheet):
        """Detect the template to be used from the sheet header"""
        templates = self.env["product.supplierinfo.import.template"].search([])
        template_headers = [(t, t._template_headers()) for t in templates]
        header_values = []
        for template, header in template_headers:
            header_values = self._parse_header(sheet.row_values(template.header_offset))
            if set(header_values) == header:
                self.template_id = template
                return header_values
        if not self.template_id:
            raise UserError(_("We couldn't find a suitable template for your file"))

    def _parse_sheet(self, data):
        """Extract the data and apply the import logic"""
        # Avoid cells with numbers which aren't decimals but end being rendered as
        # floats when passed to strings
        def row_values(row):
            values = []
            for cell in row:
                # XL_CELL_NUMBER: float
                if cell.ctype == 2 and cell.value.is_integer():
                    values.append(int(cell.value))
                    continue
                values.append(cell.value)
            return values

        workbook = xlrd.open_workbook(file_contents=data)
        sheet = workbook.sheet_by_index(0)
        header_values = self._detect_template(sheet)
        parsed_data = []
        for nrow in range(self.template_id.header_offset + 1, sheet.nrows):
            parsed_data.append(
                {
                    header: value
                    for header, value in zip(header_values, row_values(sheet.row(nrow)))
                }
            )
        return parsed_data

    def _prepare_supplierinfo_values(self, row_data):
        """Overridable hook method so we can inject general wizard values"""
        values = {
            "delay": self.delay,
            "date_start": self.date_start,
        }
        values.update(
            {
                tl.field_id.name: row_data[tl.header_name]
                for tl in self.template_id.template_line_ids
                if tl.field_id
            }
        )
        return values

    def _update_create_supplierinfo_data(self, parsed_data):
        """Create or import vendor list for the parsed data"""
        supplier_infos = self.env["product.supplierinfo"]
        for row_data in parsed_data:
            # Repeating headers...
            if (
                set(self._parse_header(row_data.values()))
                == self.template_id._template_headers()
            ):
                continue
            barcode = row_data[self.template_id.barcode_header_name]
            if isinstance(barcode, float) or isinstance(barcode, int):
                barcode = str(int(barcode))
            # Avoid surrounding spaces
            barcode = barcode.strip()
            if not barcode:
                continue
            product = (
                self.env["product.template"]
                .with_context(active_test=False)
                .search([("barcode", "=", barcode)])
            )
            if not product:
                if not self.create_new_products:
                    continue
                vendor_product_name_header = (
                    self.template_id.template_line_ids.filtered(
                        lambda x: x.field_id.name == "product_name"
                    ).header_name
                )
                vendor_product_name = row_data.get(
                    vendor_product_name_header,
                    _("%(barcode)s (product imported)", barcode=barcode),
                )
                # The product barcode could clash with a packaging barcode see
                # _check_barcode_uniqueness method.
                try:
                    product = self.env["product.template"].create(
                        {
                            "created_from_supplierinfo_import": True,
                            "name": vendor_product_name,
                            "barcode": barcode,
                            "purchase_ok": False,
                            "sale_ok": False,
                        }
                    )
                    product.message_post(
                        body=_("Created form vendor pricelist import"), type="note"
                    )
                except ValidationError:
                    _logger.warning(
                        f"The product {vendor_product_name} couldn't be created due "
                        f"to barcode collission, probably with a product package"
                    )
                    continue
            # TODO: Consider things like min_qty to refine the search
            previous_product_supplierinfo = self.env["product.supplierinfo"].search(
                [
                    ("partner_id", "=", self.supplier_id.id),
                    ("product_tmpl_id", "=", product.id),
                    "|",
                    ("date_end", "=", False),
                    ("date_end", ">=", self.date_start),
                ],
                order="date_start desc",
                limit=1,
            )
            if previous_product_supplierinfo:
                previous_product_supplierinfo.date_end = (
                    self.date_start - relativedelta(days=1)
                )
            product_supplierinfo = supplier_infos.create(
                {
                    "partner_id": self.supplier_id.id,
                    "product_tmpl_id": product.id,
                }
            )
            supplier_infos += product_supplierinfo
            try:
                product_supplierinfo.update(self._prepare_supplierinfo_values(row_data))
            except Exception:
                raise UserError(
                    _("The row format seems to be incorrect %(row)s", row=str(row_data))
                ) from Exception
        return supplier_infos

    def action_import_file(self):
        """Process the uploaded sheet"""
        self.ensure_one()
        data = base64.b64decode(self.supplierinfo_file)
        parsed_data = self._parse_sheet(data)
        supplier_infos = self._update_create_supplierinfo_data(parsed_data)
        return {
            "name": "Imported supplier infos",
            "type": "ir.actions.act_window",
            "view_type": "tree,form",
            "view_mode": "tree",
            "res_model": "product.supplierinfo",
            "domain": [("id", "in", supplier_infos.ids)],
            "context": {"visible_product_tmpl_id": False},
            "help": _(
                """<p class="o_view_nocontent">
                No vendor pricelists were created or updated.
            </p>"""
            ),
        }
