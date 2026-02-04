# Copyright 2021 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class ProductPricelistXlsx(models.AbstractModel):
    _name = "report.product_pricelist_direct_print_xlsx.report"
    _inherit = "report.report_xlsx.abstract"
    _description = "Abstract model to export as xlsx the product pricelist"

    def generate_xlsx_report(self, workbook, data, objects):
        book = objects[0].with_context(
            lang=objects[0].lang
            or self.env["res.users"].browse(objects[0].create_uid.id).lang
        )
        formats = self._prepare_formats(workbook, book)
        self = self.with_context(
            lang=book.lang or self.env["res.users"].browse(book.create_uid.id).lang
        )
        pricelist = book.get_pricelist_to_print()
        sheet = self._create_product_pricelist_sheet(workbook, book, pricelist, formats)
        sheet = self._fill_data(workbook, sheet, book, pricelist, formats)

    def _get_lang(self, user_id, lang_code=False):
        if not lang_code:
            lang_code = self.env["res.users"].browse(user_id).lang
        return self.env["res.lang"]._lang_get(lang_code)

    def _create_product_pricelist_sheet(self, workbook, book, pricelist, formats):
        sheet = workbook.add_worksheet(self.env._("PRODUCTS"))
        # Title construction
        sheet.write("A1", self.env._("Price List Name:"), formats["title"])
        if book.show_pricelist_name:
            sheet.write("A2", pricelist.name)
        else:
            sheet.write("A2", self.env._("Special Pricelist"))
        sheet.write("B1", self.env._("Currency:"), formats["title"])
        sheet.write("B2", pricelist.currency_id.name)
        sheet.write("D1", self.env._("Date:"), formats["title"])
        sheet.write("D2", book.date, formats["date"])
        # Header construction
        if book.partner_id:
            sheet.write(4, 0, book.partner_id.name, formats["header"])
        elif book.partner_ids:
            sheet.write(4, 0, book.partner_ids[0].name, formats["header"])
        header_row = self._prepare_header_row(book)
        self._set_column_widths(sheet, header_row)
        sheet.write_row(5, 0, header_row, formats["header"])
        return sheet

    def _fill_data(self, workbook, sheet, book, pricelist, formats):
        row = 6
        for group in book.get_groups_to_print():
            if book.breakage_per_category:
                sheet.write(
                    row, 0, book.get_group_name(group["group_name"]), formats["bold"]
                )
                row += 1
            for product_data in group["products"]:
                # Get product directly from product_data or inside as a dictionary
                product = (
                    product_data["product"]
                    if isinstance(product_data, dict)
                    else product_data
                )
                row_with_formats = self._prepare_data_row_with_formats(
                    book, product, formats
                )
                for i, cell_with_format in enumerate(row_with_formats):
                    cell_value, format_ = cell_with_format
                    sheet.write(row, i, cell_value, format_)
                row += 1
        if book.summary:
            sheet.write(row, 0, self.env._("Summary:"), formats["bold"])
            sheet.write(row + 1, 0, book.summary)
        return sheet

    def _prepare_formats(self, workbook, book):
        lang = self._get_lang(book.create_uid.id, lang_code=book.lang)
        date_format = (
            lang.date_format.replace("%d", "dd")
            .replace("%m", "mm")
            .replace("%Y", "YYYY")
            .replace("/", "-")
        )
        return {
            "title": workbook.add_format(
                {"bold": 1, "border": 1, "align": "left", "valign": "vjustify"}
            ),
            "header": workbook.add_format(
                {
                    "bold": 1,
                    "border": 1,
                    "align": "center",
                    "valign": "vjustify",
                    "fg_color": "#F2F2F2",
                }
            ),
            "date": workbook.add_format({"num_format": date_format}),
            "bold": workbook.add_format({"bold": 1}),
            "decimal": workbook.add_format({"num_format": "0.00"}),
            "decimal_bold": workbook.add_format({"num_format": "0.00", "bold": 1}),
        }

    def _prepare_header_row(self, book):
        _ = self.env._
        row = [_("Description")]
        if book.show_internal_category:
            row.append(_("Internal Category"))
        if book.show_standard_price:
            row.append(_("Cost Price"))
        if book.show_sale_price:
            row.append(_("Sale Price"))
        row.append(_("List Price"))
        if book.show_product_uom:
            row.append(_("UoM"))
        return row

    def _prepare_data_row_with_formats(self, book, product, formats):
        row = [(product.display_name, None)]
        if book.show_internal_category:
            row.append((product.categ_id.display_name, None))
        if book.show_standard_price:
            row.append((product.standard_price, formats["decimal"]))
        if book.show_sale_price:
            row.append((product.list_price, formats["decimal"]))
        row.append(
            (
                book.with_context(product=product).product_price,
                formats["decimal_bold"],
            )
        )
        if book.show_product_uom:
            row.append((product.uom_id.name, formats["bold"]))
        return row

    def _set_column_widths(self, sheet, header_row):
        # Special label with wider column
        description_label = self.env._("Description")
        for i, label in enumerate(header_row):
            width = 45 if label == description_label else 15
            sheet.set_column(i, i, width)
