# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductPricelistItem(models.Model):
    _inherit = ['abstract.pricelist.item.generator', 'product.pricelist.item']
    _name = 'product.pricelist.item'

    auto = fields.Boolean(
        string='Auto',
        help="If true, the item pricelist was built automatically "
             "with Pricelist")
    item_template_id = fields.Many2one(
        comodel_name='pricelist.item.template',
        string='Item template', readonly=True, ondelete='cascade')
    product_condition_id = fields.Many2one(
        comodel_name='pricelist.product.condition',
        string='Product condition', readonly=True, ondelete='cascade')


class ProductPricelistVersion(models.Model):
    _inherit = 'product.pricelist.version'

    item_auto_ids = fields.One2many(
        comodel_name='product.pricelist.item', inverse_name='price_version_id',
        string='Pricelist items auto', domain=[('auto', '=', True)],
        help="Automatic built items")
    item_manual_ids = fields.One2many(
        comodel_name='product.pricelist.item', inverse_name='price_version_id',
        string='Pricelist items manual', domain=[('auto', '=', False)],
        help="Manually created items")
