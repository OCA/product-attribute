# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _compute_tax_id(self):
        super()._compute_tax_id()
        for line in self:
            line.tax_id = [
                (
                    6,
                    0,
                    line.tax_id.ids + line.product_id.additional_tax_ids.ids,
                )
            ]
