# Copyright 2018 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.onchange('extra_weight')
    def _onchange_extra_weight(self):
        if self.is_weight_uom:
            self.weight = self.uom_id.factor_inv + self.extra_weight
        else:
            self.weight = self.weight + self.extra_weight

    @api.multi
    def write(self, vals):
        if vals.get('uom_id') or vals.get('extra_weight'):
            uom_id = (self.env['product.uom'].browse(vals.get('uom_id')) or
                      self.uom_id)
            if self.is_weight_uom:
                vals['weight'] = uom_id.factor_inv + (
                    vals.get('extra_weight') or self.extra_weight)
        return super().write(vals)

    @api.model
    def create(self, vals):
        template = self.env['product.template'].browse(
            vals.get('product_tmpl_id'))
        uom_id = template.is_weight_uom and template.uom_id
        if not template:
            uom_id = (self.env['product.uom'].browse(vals.get('uom_id')))
        if uom_id and uom_id.category_id == self.env.ref(
                'product.product_uom_categ_kgm'):
            vals['weight'] = uom_id.factor_inv + (
                vals.get('extra_weight') or template.extra_weight)
        return super().create(vals)
