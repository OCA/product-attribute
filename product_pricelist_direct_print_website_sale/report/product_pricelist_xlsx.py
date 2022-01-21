# Copyright 2022 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, models


class ProductPricelistXlsx(models.AbstractModel):
    _inherit = "report.product_pricelist_direct_print.product_pricelist_xlsx"

    def _add_extra_header(self, sheet, book, next_col, header_format):
        next_col = super()._add_extra_header(sheet, book, next_col, header_format)
        if book.show_public_category:
            next_col += 1
            sheet.write(5, next_col, _("Public Category"), header_format)
        return next_col

    def _add_extra_info(self, sheet, book, product, row, next_col):
        next_col = super()._add_extra_info(sheet, book, product, row, next_col)
        if book.show_public_category:
            next_col += 1
            if product.public_categ_ids:
                sheet.write(row, next_col, product.public_categ_ids[:1].display_name)
        return next_col
