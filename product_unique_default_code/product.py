# -*- coding: utf-8 -*-
# © 2016 initOS Gmb
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class product_product(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char('Internal Reference', copy=False)

    @api.multi
    @api.constrains('default_code')
    def _check_unique(self):
        for obj in self:
            if 1 < self.search_count(
                    [('default_code', '=', obj.default_code)]):
                raise UserError(_("Internal Reference must be unique!"))
