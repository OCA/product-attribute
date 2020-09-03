import json
from odoo import api, fields, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    replacement_info_widget = fields.Text(compute='_compute_replacement_info')
    show_replacement = fields.Boolean(compute='_compute_replacement_info')

    @api.multi
    @api.depends('product_id')
    def _compute_replacement_info(self):
        for so in self:
            if so.product_id.lifecycle_state == 'obsolete':
                so.show_replacement = True
                replacement = so.product_id.get_good_replacements()
                info = {
                    'state': so.product_id.lifecycle_state,
                    'product_qty': so.product_id.qty_available,
                    'replaced_by': '%s%s' % ('[%s] ' % replacement.default_code or '', replacement.name
                                             ) if replacement else False,
                    'product_id': replacement.id,
                }
                so.replacement_info_widget = json.dumps(info)
            else:
                so.replacement_info_widget = json.dumps(False)
                so.show_replacement = False
