# Copyright 2018 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    extra_weight = fields.Float(
        'Extra Weight',
        compute='_compute_extra_weight',
        inverse='_inverse_extra_weight',
        digits=dp.get_precision('Stock Weight'),
        help="Extra weight (in Kg.) given by packaging, etc.",
    )
    is_weight_uom = fields.Boolean(
        compute='_compute_is_weight_uom',
        readonly=True,
        default=False,
    )

    @api.depends('product_variant_ids', 'product_variant_ids.weight')
    def _compute_extra_weight(self):
        unique_variants = self.filtered(
            lambda x: len(x.product_variant_ids) == 1)
        for template in unique_variants:
            template.extra_weight = template.product_variant_ids.extra_weight
        (self - unique_variants).update({'extra_weight': 0.0})

    @api.multi
    def _inverse_extra_weight(self):
        for template in self.filtered(
                lambda x: len(x.product_variant_ids) == 1):
            template.product_variant_ids.extra_weight = template.extra_weight

    @api.depends('uom_id', 'uom_id.category_id')
    def _compute_is_weight_uom(self):
        product_uom_categ_kgm = self.env.ref('product.product_uom_categ_kgm')
        for product in self:
            product.is_weight_uom = (
                product.uom_id.category_id == product_uom_categ_kgm)

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
            self.extra_weight = 0

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
