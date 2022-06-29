
from odoo import api, fields, models


class ProductTemplateTag(models.Model):

    _inherit = 'product.template.tag'

    product_ids = fields.Many2many(
        comodel_name='product.product', string="Products",
        relation='product_variant_product_tag_rel',
        column1='tag_id', column2='product_id')
    variants_count = fields.Integer(
        string="# of Variants", compute='_compute_variants_count')

    @api.multi
    @api.depends('product_ids')
    def _compute_variants_count(self):
        if not self.ids:
            return
        self.env.cr.execute("""SELECT tag_id, COUNT(*)
            FROM product_variant_product_tag_rel
            WHERE tag_id IN %s
            GROUP BY tag_id""", (tuple(self.ids),))
        tag_id_product_count = dict(self.env.cr.fetchall())
        for rec in self:
            rec.variants_count = tag_id_product_count.get(rec.id, 0)
