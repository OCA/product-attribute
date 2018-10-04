# -*- coding: utf-8 -*-
from openerp import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        select_type = self._context.get('select_type', False)
        if select_type:
            res.update({
                'customer': select_type == 'customer',
                'supplier': select_type == 'supplier',
            })
        return res
