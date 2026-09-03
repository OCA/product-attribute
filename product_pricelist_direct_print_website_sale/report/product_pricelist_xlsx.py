# Copyright 2022 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class ProductPricelistXlsx(models.AbstractModel):
    _inherit = "report.product_pricelist_direct_print_xlsx.report"

    def _prepare_header_row(self, book):
        row = super()._prepare_header_row(book)
        if book.show_public_category:
            row.append(self.env._("Public Category"))
        return row

    def _prepare_data_row_with_formats(self, book, product, formats):
        row = super()._prepare_data_row_with_formats(book, product, formats)
        if book.show_public_category:
            row.append((product.public_categ_ids[:1].display_name, None))
        return row
