# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    product_brand_id = fields.Many2one(
        comodel_name='product.brand',
        string='Brand',
    )

    def _select(self):
        select_str = super()._select()
        select_str += """
            , product_brand_id as product_brand_id
            """
        return select_str


    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += ", template.product_brand_id"
        return group_by_str
