# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class ProductKosher(models.Model):
    _name = "product.kosher"
    _description = "Product Kosher"
    _order = "date_start desc"

    name = fields.Char(
        string="# Certificate",
        required=True,
    )
    product_tmpl_id = fields.Many2one(
        string="Product Template",
        comodel_name="product.template",
        ondelete="cascade",
        required=True
    )
    date_start = fields.Date(
        string="Start Date",
        required=True
    )
    date_end = fields.Date(
        string="End Date"
    )

    @api.constrains(
        "date_start", "date_end")
    def _check_date(self):
        strWarning = _(
            "'Date End' must be greater than 'Date Start'")
        if self.date_start and self.date_end:
            if self.date_start > self.date_end:
                raise UserError(strWarning)
