
from odoo import fields, models


class Product(models.Model):

    _inherit = 'product.product'

    tag_ids = fields.Many2many(
        comodel_name='product.template.tag', string="Product Tags",
        relation='product_variant_product_tag_rel',
        column1='product_id', column2='tag_id')
