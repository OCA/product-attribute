# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64
import logging

import xlrd
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import parse_version

_logger = logging.getLogger(__name__)


class ProductSupplierInfoImport(models.TransientModel):
    _name = "product.supplierinfo.import"
    _description = "Import supplier info records"

    supplier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Supplier",
        compute="_compute_supplier_id",
        store=True,
        readonly=False,
    )
    date_start = fields.Date(string="Validity", required=True)
    delay = fields.Integer()
    create_new_products = fields.Boolean(
        help="If a product isn't found by its Search Field, it will be created with the "
        "provided data",
        default=True,
    )
    supplierinfo_file = fields.Binary(required=True)
    supplierinfo_filename = fields.Char()
    template_id = fields.Many2one(
        comodel_name="product.supplierinfo.import.template",
        compute="_compute_template_id",
        store=True,
    )

    @api.depends("template_id")
    def _compute_supplier_id(self):
        for record in self:
            if record.template_id.supplier_id:
                record.supplier_id = record.template_id.supplier_id

    @api.depends("supplierinfo_file")
    def _compute_template_id(self):
        for record in self:
            if record.supplierinfo_file:
                filename = record.supplierinfo_filename or ""
                if parse_version(xlrd.__version__) >= parse_version(
                    "2.0"
                ) or not filename.lower().endswith(".xlsx"):
                    raise UserError(_("Only .xlsx files are supported."))
                data = base64.b64decode(record.supplierinfo_file)
                workbook = xlrd.open_workbook(file_contents=data)
                record._detect_template(workbook)
            else:
                record.template_id = False

    @api.model
    def _parse_header(self, header):
        # Trim left and right blank chars and convert newlines for better matching
        return [str(h).replace("\n", " ").strip() for h in header]

    def _detect_template(self, workbook):
        """Detect the template to be used from the sheet header"""
        templates = self.env["product.supplierinfo.import.template"].search([])
        template_headers = [(t, t._template_headers()) for t in templates]
        header_values = []
        for template, header in template_headers:
            if template.sheet_number - 1 >= workbook.nsheets:
                raise UserError(
                    _(
                        f"Sheet number {template.sheet_number} is out of range. "
                        f"The workbook only has {workbook.nsheets} sheets."
                    )
                )
            sheet = workbook.sheet_by_index(template.sheet_number - 1)
            header_values = self._parse_header(sheet.row_values(template.header_offset))
            if set(header_values) == header:
                self.template_id = template
                return header_values
        if not self.template_id:
            raise UserError(
                _(
                    f"No matching template for these header columns.\n"
                    f"Total header columns: {', '.join(header_values)}"
                )
            )

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
        header_values = self._detect_template(workbook)
        sheet = workbook.sheet_by_index(self.template_id.sheet_number - 1)
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
            tl.sudo().field_id.name: row_data.get(
                self._parse_header([tl.header_name])[0], ""
            )
            for tl in self.template_id.template_line_ids
            if tl.sudo().field_id
        }
        # Avoid rows where there's no information given
        all_values_with_content = all([x not in {None, ""} for x in values.values()])
        if not all_values_with_content:
            return
        values.update(
            {
                "delay": self.delay,
                "date_start": self.date_start,
            }
        )
        return values

    def _update_create_supplierinfo_data(self, parsed_data):
        """Create or import vendor list for the parsed data"""
        supplier_infos = self.env["product.supplierinfo"]
        all_supplier_infos = self.env["product.supplierinfo"].search(
            [("partner_id", "=", self.supplier_id.id)]
        )
        search_field = self.template_id.sudo().import_criteria_field_id.name
        for row_data in parsed_data:
            # Repeating headers...
            if (
                set(self._parse_header(row_data.values()))
                == self.template_id._template_headers()
            ):
                continue
            search_value = row_data[self.template_id.search_header_name]
            if isinstance(search_value, float) or isinstance(search_value, int):
                search_value = str(int(search_value))
            # Avoid surrounding spaces
            search_value = search_value.strip()
            if not search_value:
                continue
            product = (
                self.env["product.template"]
                .with_context(active_test=False)
                .search([(search_field, "=", search_value)], limit=1)
            )
            if not product and self.create_new_products:
                product = self._create_new_product(search_value, row_data, search_field)
                if not product:
                    continue
            previous_supplierinfo = self.env["product.supplierinfo"].search(
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
            if self.template_id.only_update_existing and previous_supplierinfo:
                supplier_infos += self._update_existing_supplierinfo(
                    previous_supplierinfo, row_data
                )
            else:
                new_supplier_info = self._create_new_supplierinfo(
                    previous_supplierinfo, product, row_data, search_field, search_value
                )
                if new_supplier_info:
                    supplier_infos += new_supplier_info
        unchanged_supplier_infos = all_supplier_infos - supplier_infos
        unchanged_supplier_infos.write({"import_status": "unchanged"})
        return supplier_infos, unchanged_supplier_infos

    def _create_new_product(self, search_value, row_data, search_field):
        """Creates a new product if allowed."""
        vendor_product_name_header = self.template_id.template_line_ids.filtered(
            lambda x: x.sudo().field_id.name == "product_name"
        ).header_name
        vendor_product_name = row_data.get(
            vendor_product_name_header,
            _("%(code)s (product imported)", code=search_value),
        )
        product_data = {
            "created_from_supplierinfo_import": True,
            "name": vendor_product_name,
            "purchase_ok": False,
            "sale_ok": False,
            search_field: search_value,
        }
        try:
            product = self.env["product.template"].create(product_data)
            product.message_post(
                body=_("Created from supplier price list import"),
                type="note",
            )
            return product
        except ValidationError:
            _logger.warning(
                f"The product {vendor_product_name}"
                f" could not be created due to a {search_field} collision."
            )
            return self.env["product.product"]

    def _update_existing_supplierinfo(self, supplierinfo, row_data):
        """Updates an existing supplier price list record."""
        supplierinfo.write(self._prepare_supplierinfo_values(row_data))
        supplierinfo.import_status = "new_or_updated"
        return supplierinfo

    def _create_new_supplierinfo(
        self, previous_supplierinfo, product, row_data, search_field, search_value
    ):
        """Creates a new supplier price list record, updating the previous one if needed."""
        values = self._prepare_supplierinfo_values(row_data)
        if not values:
            return self.env["product.supplierinfo"]
        if previous_supplierinfo:
            previous_supplierinfo.date_end = self.date_start - relativedelta(days=1)
        product_supplierinfo = self.env["product.supplierinfo"].create(
            {
                "partner_id": self.supplier_id.id,
                "product_tmpl_id": product.id,
                "import_status": "new_or_updated",
                **(
                    {search_field: search_value}
                    if search_field in self.env["product.supplierinfo"]._fields
                    else {}
                ),
            }
        )
        product_supplierinfo.write(values)
        return product_supplierinfo

    def action_import_file(self):
        """Process the uploaded sheet"""
        self.ensure_one()
        data = base64.b64decode(self.supplierinfo_file)
        parsed_data = self._parse_sheet(data)
        (
            supplier_infos,
            unchanged_supplier_infos,
        ) = self._update_create_supplierinfo_data(parsed_data)
        if self.template_id.show_not_updated_rates:
            domain = [("id", "in", supplier_infos.ids + unchanged_supplier_infos.ids)]
            context = {"group_by": ["import_status"]}
        else:
            domain = [("id", "in", supplier_infos.ids)]
            context = {}
        context.update({"visible_product_tmpl_id": False})
        return {
            "name": "Imported supplier infos",
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "product.supplierinfo",
            "domain": domain,
            "context": context,
            "help": _(
                """<p class="o_view_nocontent">
                No vendor pricelists were created or updated.
            </p>"""
            ),
        }
