# -*- coding: utf-8 -*-
# Copyright (C) 2009  Àngel Àlvarez - NaN  (http://www.nan-tic.com)
#                     All Rights Reserved.
# © 2015 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def copy(self, default=None):
        """Unlink pack lines that should not be copied."""
        self.ensure_one()
        sale_copy = super(SaleOrder, self).copy(default)
        sale_copy.order_line.filtered(
            lambda r: r.pack_parent_line_id.order_id == self).unlink()
        return sale_copy
