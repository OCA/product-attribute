# Copyright (C) 2020-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    tmpl_company_id = fields.Many2one(
        related="product_tmpl_id.company_id",
        string="Company of the related Template",
        store=True)

    @api.model_cr_context
    def _auto_init(self):
        found = -1
        i = 0
        for _sql_constraint in self._sql_constraints:
            if _sql_constraint[0] == "barcode_uniq":
                found = i
            i += 1
        if found != -1:
            self._sql_constraints[found] = (
                "barcode_uniq",
                "unique(barcode, tmpl_company_id)", _(
                    "A barcode can only be assigned to one"
                    " product per company !")
            )
        return super()._auto_init()
