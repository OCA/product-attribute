# -*- coding: utf-8 -*-
# © 2016 initOS Gmb
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from openerp import models, api, _
from openerp.exceptions import Warning


class Product(models.Model):
    _inherit = 'product.product'

    @api.multi
    @api.constrains('default_code')
    def _check_unique(self):
        for obj in self:
            if 1 < self.search_count([('default_code', '=', obj.default_code)]):
                raise Warning(_("Internal Reference must be unique!"))
