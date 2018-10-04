import openerp.addons.decimal_precision as dp
from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    volume = fields.Float('Volume', help="The volume in m3.",
                          digits=dp.get_precision('Product Volume'))


class ProductProduct(models.Model):
    _inherit = 'product.product'

    weight_volumetric = fields.Float(
        string='Volumetric weight',
        store=True, readonly=True,
        digits=dp.get_precision('Product Volume'))
