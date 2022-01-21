# Copyright 2021 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, fields, models


class ProductPricelistXlsx(models.AbstractModel):
    _name = "report.product_pricelist_direct_print.product_pricelist_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Abstract model to export as xlsx the product pricelist"

    def _get_lang(self, user_id):
        lang_code = self.env["res.users"].browse(user_id).lang
        return self.env["res.lang"]._lang_get(lang_code)

    def _create_product_pricelist_sheet(self, workbook, book, pricelist):
        title_format = workbook.add_format(
            {"bold": 1, "border": 1, "align": "left", "valign": "vjustify"}
        )
        header_format = workbook.add_format(
            {
                "bold": 1,
                "border": 1,
                "align": "center",
                "valign": "vjustify",
                "fg_color": "#F2F2F2",
            }
        )
        lang = self._get_lang(book.create_uid.id)
        date_format = lang.date_format.replace("%d", "dd")
        date_format = date_format.replace("%m", "mm")
        date_format = date_format.replace("%Y", "YYYY")
        date_format = date_format.replace("/", "-")
        date_format = workbook.add_format({"num_format": date_format})
        sheet = workbook.add_worksheet(_("PRODUCTS"))
        sheet.set_column("A:A", 45)
        sheet.set_column("B:H", 15)
        # Title construction
        sheet.write("A1", _("Price List Name:"), title_format)
        if not book.hide_pricelist_name:
            sheet.write("A2", pricelist.name)
        else:
            sheet.write("A2", _("Special Pricelist"))
        sheet.write("B1", _("Currency:"), title_format)
        sheet.write("B2", pricelist.currency_id.name)
        sheet.write("D1", _("Date:"), title_format)
        if book.date:
            sheet.write("D2", book.date, date_format)
        else:
            sheet.write("D2", book.create_date, date_format)
        # Header construction
        if book.partner_id:
            sheet.write(4, 0, book.partner_id.name, header_format)
        elif book.partner_ids:
            sheet.write(4, 0, book.partner_ids[0].name, header_format)
        next_col = 0
        sheet.write(5, next_col, _("Description"), header_format)
        next_col = self._add_extra_header(sheet, book, next_col, header_format)
        if book.show_internal_category:
            next_col += 1
            sheet.write(5, next_col, _("Internal Category"), header_format)
        if book.show_standard_price:
            next_col += 1
            sheet.write(5, next_col, _("Cost Price"), header_format)
        if book.show_sale_price:
            next_col += 1
            sheet.write(5, next_col, _("Sale Price"), header_format)
        next_col += 1
        sheet.write(5, next_col, _("List Price"), header_format)
        return sheet

    def _add_extra_header(self, sheet, book, next_col, header_format):
        return next_col

    def _fill_data(self, workbook, sheet, book, pricelist):
        bold_format = workbook.add_format({"bold": 1})
        decimal_format = workbook.add_format({"num_format": "0.00"})
        decimal_bold_format = workbook.add_format({"num_format": "0.00", "bold": 1})
        row = 6
        # We should avoid sending a date as a False object as it will crash if a
        # submethod tries to make comparisons with other date.
        print_date = book.date or fields.Date.today()
        for group in book.get_groups_to_print():
            if book.breakage_per_category:
                sheet.write(row, 0, group["group_name"], bold_format)
                row += 1
            for product in group["products"]:
                next_col = 0
                sheet.write(row, next_col, product.display_name)
                next_col = self._add_extra_info(sheet, book, product, row, next_col)
                if book.show_internal_category:
                    next_col += 1
                    sheet.write(row, next_col, product.categ_id.display_name)
                if book.show_standard_price:
                    next_col += 1
                    sheet.write(row, next_col, product.standard_price, decimal_format)
                if book.show_sale_price:
                    next_col += 1
                    sheet.write(row, next_col, product.list_price, decimal_format)
                next_col += 1
                sheet.write(
                    row,
                    next_col,
                    product.with_context(pricelist=pricelist.id, date=print_date).price,
                    decimal_bold_format,
                )
                row += 1
        if book.summary:
            sheet.write(row, 0, _("Summary:"), bold_format)
            sheet.write(row + 1, 0, book.summary)
        return sheet

    def _add_extra_info(self, sheet, book, product, row, next_col):
        return next_col

    def generate_xlsx_report(self, workbook, data, objects):
        book = objects[0]
        pricelist = book.get_pricelist_to_print()
        sheet = self._create_product_pricelist_sheet(workbook, book, pricelist)
        sheet = self._fill_data(workbook, sheet, book, pricelist)
