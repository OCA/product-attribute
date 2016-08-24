# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import _, api, fields, models


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    bundle_id = fields.Many2one(
        comodel_name="product.product", string="Product bundle",
        readonly=True)

    @api.model
    def _run(self, procurement):
        if (procurement.rule_id.action == 'move' and
                procurement.product_id.bundle_ok):
            if not procurement.rule_id.location_src_id:
                self.message_post(
                    procurement.ids, body=_('No source location defined!'))
                return False
            move_obj = self.env['stock.move'].sudo()
            move_vals = self._run_move_create(procurement)
            for component in procurement.product_id.bundle_line_ids:
                component_vals = move_vals.copy()
                component_vals.update({
                    'product_id': component.product_id.id,
                    'product_uom_qty': (
                        component.qty * move_vals['product_uom_qty']),
                    'bundle_id': procurement.product_id.id,
                })
                move_obj.create(component_vals)
            return True
        return super(ProcurementOrder, self)._run(procurement)
