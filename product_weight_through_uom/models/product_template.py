# Copyright 2018 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    extra_weight = fields.Float(
        'Extra Weight',
        digits=dp.get_precision('Stock Weight'),
        help="Extra weight (in Kg.) given by packaging, etc.",
    )
    is_weight_uom = fields.Boolean(
        compute='_compute_is_weight_uom',
        readonly=True,
        default=False,
    )

    @api.depends('uom_id.category_id')
    def _compute_is_weight_uom(self):
        product_uom_categ_kgm = self.env.ref('product.product_uom_categ_kgm')
        for product in self:
            if product.uom_id.category_id == product_uom_categ_kgm:
                product.is_weight_uom = True

    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        super()._onchange_uom_id()
        # When a UoM is in Weight category, we set the product weight to its
        # corresponding conversion to Kg.
        if self.is_weight_uom:
            self.weight = self.uom_id.factor_inv + self.extra_weight

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
        if vals.get('uom_id') or vals.get('extra_weight'):
            uom_id = self.env['product.uom'].browse(vals.get('uom_id'))
            if uom_id.category_id == self.env.ref(
                    'product.product_uom_categ_kgm'):
                vals['weight'] = uom_id.factor_inv + vals.get(
                    'extra_weight', 0)
        return super().create(vals)
