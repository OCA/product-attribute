# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning as UserError
from .product_condition import update_item_tpl_or_condition, TODO_SELECTION


class AbstractPricelistItemGenerator(models.AbstractModel):
    _name = "abstract.pricelist.item.generator"
    _description = "Abstract Pricelist Items Generator"

    price_generator_id = fields.Many2one(
        comodel_name='pricelist.item.generator',
        string='Generator', readonly=True)
    min_quantity = fields.Integer(default=1)


class PricelistItemTemplateBase(models.Model):
    _name = 'pricelist.item.template'
    _description = "Pricelist item template"
    _rec_name = 'id'

    _order = "sequence, min_quantity desc"

    sequence = fields.Integer(
        string='Sequence', required=True, default=50,
        help="Gives the order in which the pricelist items will be checked"
             "by the ERP.\n"
             "The evaluation gives highest priority to lowest sequence and "
             "stops as soon as a matching price item is found.")
    base = fields.Selection(
        selection='_price_field_get', default=1,
        string='Based on', required=True, size=-1,
        help="Base price for computation.")
    base_pricelist_id = fields.Many2one(
        comodel_name='product.pricelist', string='Other PL',
        help="Other pricelist on which this item is based.")
    price_surcharge = fields.Float(
        string='Price Surcharge',
        digits_compute=dp.get_precision('Product Price'),
        help='Specify the fixed amount to add or substract(if negative) to '
             'the amount calculated with the discount.')
    price_discount = fields.Float(
        string='Discount (%)', digits=(16, 2), default=0)
    price_round = fields.Float(
        string='Price Rounding',
        digits_compute=dp.get_precision('Product Price'),
        help="Sets the price so that it is a multiple of this value.\n"
             "Rounding is applied after the discount and before the "
             "surcharge.\n To have prices that end in 9.99, "
             "set rounding 10, surcharge -0.01")
    price_min_margin = fields.Float(
        string='Min. Price Margin',
        digits_compute=dp.get_precision('Product Price'),
        help='Specify the minimum amount of margin over the base price.')
    price_max_margin = fields.Float(
        string='Max. Price Margin',
        digits_compute=dp.get_precision('Product Price'),
        help='Specify the maximum amount of margin over the base price.')
    todo = fields.Selection(
        selection=TODO_SELECTION, readonly=True, string='Next Action',
        help="Required action on Pricelist Items")

    @api.one
    @api.constrains('price_min_margin', 'price_max_margin')
    def _check_margin(self):
        if self.price_max_margin and self.price_min_margin and (
                self.price_min_margin > self.price_max_margin):
            raise UserError(_("Error! The minimum margin should be lower "
                              "than the maximum margin."))

    @api.one
    @api.constrains('price_discount', 'price_surcharge')
    def _check_price_elements(self):
        # check price validity
        if self.price_discount == 0 and self.price_surcharge == 0:
            raise UserError(
                _("'Discount' or 'Surcharge' must be different from 0."))

    @api.model
    def _price_field_get(self):
        # TODO future version : support other type of pricelists
        result = []
        result.extend([(1, _('Public Price')), (-1, _('Other Pricelist'))])
        return result


class PricelistItemTemplate(models.Model):
    """ This model is called by a second class
    """
    _inherit = ['abstract.pricelist.item.generator', 'pricelist.item.template']
    _name = 'pricelist.item.template'

    _order = 'sequence ASC, id ASC'

    price_generator_id = fields.Many2one(
        comodel_name='pricelist.item.generator', required=True)

    @api.model
    def create(self, vals):
        self.env['pricelist.item.generator'].browse(
            vals['price_generator_id']).write({'to_update': True})
        vals['todo'] = 'create'
        return super(PricelistItemTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        # Some records shouldn't be written with the same values
        todo_update = update_item_tpl_or_condition(self, vals)
        super(PricelistItemTemplate, self).write(vals)
        if todo_update:
            super(PricelistItemTemplate, todo_update).write(
                {'todo': 'update'})
        return True
