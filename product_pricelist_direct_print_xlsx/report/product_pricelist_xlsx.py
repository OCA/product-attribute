# Copyright 2021 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, models


class ProductPricelistXlsx(models.AbstractModel):
    _name = "report.product_pricelist_direct_print_xlsx.report"
    _inherit = "report.report_xlsx.abstract"
    _description = "Abstract model to export as xlsx the product pricelist"

    def _get_lang(self, user_id, lang_code=False):
        if not lang_code:
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
        lang = self._get_lang(book.create_uid.id, lang_code=book.lang)
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
        if book.show_pricelist_name:
            sheet.write("A2", pricelist.name)
        else:
            sheet.write("A2", _("Special Pricelist"))
        sheet.write("B1", _("Currency:"), title_format)
        sheet.write("B2", pricelist.currency_id.name)
        sheet.write("D1", _("Date:"), title_format)
        sheet.write("D2", book.date, date_format)
        # Header construction
        header_values = self._get_header_values(book)
        for column, value in enumerate(header_values):
            sheet.write(5, column, value, header_format)
        return sheet

    def _get_price_headers(self, book):
        # Defaults to `List Price`
        return [
            _("List Price"),
        ]

    def _get_price_values(self, book, product, formats):
        pricelist = book.get_pricelist_to_print()
        decimal_bold_format = formats.get("decimal_format")
        return [
            (
                book.get_price_for_pricelist(pricelist, product),
                decimal_bold_format,
            )
        ]

    def _add_extra_header(self, book):
        # Add extra columns right after product's column
        return []

    def _add_extra_info(self, book, product, **kw):
        # Add extra values right after product's name
        return []

    def _get_header_values(self, book):
        res = []
        if book.partner_id:
            res.append(book.partner_id.name)
        elif book.partner_ids:
            res.append(book.partner_ids[0].name)
        res.append(_("Description"))
        res.extend(self._add_extra_header(book))
        if book.show_internal_category:
            res.append(_("Internal Category"))
        if book.show_standard_price:
            res.append(_("Cost Price"))
        if book.show_sale_price:
            res.append(_("Sale Price"))
        res.extend(self._get_price_headers(book))
        if book.show_product_uom:
            res.append(_("UoM"))
        return res

    def _get_row_values(self, book, product, formats):
        # Returns a list of values, with an optional format which must be set to
        # [(value, format/None)]
        bold_format = formats.get("bold_format")
        decimal_format = formats.get("decimal_format")
        formats.get("decimal_format")
        default_format = formats.get("default_format")
        values = [
            (product.display_name, default_format),
        ]
        values.extend(self._add_extra_info(book, product, **formats))
        if book.show_internal_category:
            values.append((product.categ_id.display_name, default_format))
        if book.show_standard_price:
            values.append((product.standard_price, decimal_format))
        if book.show_sale_price:
            values.append((product.list_price, decimal_format))
        values.extend(self._get_price_values(book, product, formats))
        if book.show_product_uom:
            values.append((product.uom_id.name, bold_format))
        return values

    def _fill_data(self, workbook, sheet, book):
        bold_format = workbook.add_format({"bold": 1})
        decimal_format = workbook.add_format({"num_format": "0.00"})
        decimal_bold_format = workbook.add_format({"num_format": "0.00", "bold": 1})
        row = 6
        formats = {
            "bold_format": bold_format,
            "decimal_format": decimal_format,
            "decimal_bold_format": decimal_bold_format,
        }
        for group in book.get_groups_to_print():
            if book.breakage_per_category:
                sheet.write(
                    row, 0, book.get_group_name(group["group_name"]), bold_format
                )
                row += 1
            for product in group["products"]:
                row_values = self._get_row_values(book, product, formats)
                for column, (value, _format) in enumerate(row_values):
                    sheet.write(row, column, value, _format)
                row += 1
        if book.summary:
            sheet.write(row, 0, _("Summary:"), bold_format)
            sheet.write(row + 1, 0, book.summary)
        return sheet

    def generate_xlsx_report(self, workbook, data, objects):
        book = objects[0].with_context(
            lang=objects[0].lang
            or self.env["res.users"].browse(objects[0].create_uid.id).lang
        )
        self = self.with_context(
            lang=book.lang or self.env["res.users"].browse(book.create_uid.id).lang
        )
        pricelist = book.get_pricelist_to_print()
        sheet = self._create_product_pricelist_sheet(workbook, book, pricelist)
        sheet = self._fill_data(workbook, sheet, book)
