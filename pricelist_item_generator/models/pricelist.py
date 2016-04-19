# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api, _
from openerp.exceptions import Warning as UserError
import openerp.addons.decimal_precision as dp
from collections import defaultdict


TODO_SELECTION = [('update', 'Update'), ('create', 'Create')]


def update_item_tpl_or_condition(vals, self):
    """ Called by write method of 'pricelist.item.template'
                              and 'pricelist.product.condition' models
    """
    # objects used for future write() with {'todo': 'update'}
    todo_update = self.env[self._name].browse(False)
    if not(len(vals) == 1 and 'todo' in vals):
        self.price_generator_id.write({'to_update': True})
        # some records should be flagged as 'update'
        for object in self:
            # if not yet created, no reason to update, we stay as 'create'
            if object.todo != 'create':
                todo_update |= object
    return todo_update


class PricelistItemGenerator(models.Model):
    _name = "pricelist.item.generator"
    _description = "Pricelist Items Generator"

    sequence = fields.Integer(
        string='Sequence', default=5,
        help="Used to generate the sequence of the price item")
    name = fields.Char(
        string='Name', required=True,
        help="Copied towards pricelist price item")
    active = fields.Boolean(
        string='Active', default=False, copy=False,
        help="If checked, rules are exported towards "
             "'Product pricelist items'")
    to_update = fields.Boolean(
        string='To update', readonly=True, default=True, copy=False,
        help="Flag if the pricelist items needs to be build")
    price_version_id = fields.Many2one(
        comodel_name='product.pricelist.version',
        string='Pricelist version', required=True,
        domain="[('pricelist_id.type', '=', 'sale')]",
        help="Only pricelist of 'Sale' type")
    copy_product_condition = fields.Boolean(
        string="Copy Involved Products", copy=False,
        help="Check to copy 'involved products' in case of "
             "duplication of generator")
    copy_item_template = fields.Boolean(
        string="Copy Price Items", copy=False,
        help="Check to copy 'price items' in case of "
             "duplication of generator")
    product_condition_ids = fields.One2many(
        comodel_name='pricelist.product.condition',
        inverse_name='price_generator_id',
        string='Product conditions',
        help="In which products are applied the price elements")
    item_template_ids = fields.One2many(
        comodel_name='pricelist.item.template',
        inverse_name='price_generator_id',
        string='Pricelist item templates',
        help="Pricelist item template")

    _sql_constraints = [
        ('name_uniq', 'unique(name)',
         "'Name' field must be unique by generator"),
    ]

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default['name'] = '%s (Copy)' % self.name
        # Conditional One2many copy
        if self.copy_item_template:
            default['item_template_ids'] = self._get_o2m_values(
                self.item_template_ids, 'item_template_id')
        if self.copy_product_condition:
            default['product_condition_ids'] = self._get_o2m_values(
                self.product_condition_ids, 'product_condition_id')
        return super(PricelistItemGenerator, self).copy(default)

    @api.multi
    def _get_o2m_values(self, objects, field_name):
        """ get values from One2many"""
        self.ensure_one()
        values = self._get_vals_from_objs(objects)
        values = [{y: z for y, z in dic.items() if y != field_name}
                  for dic in values]
        return [(0, 0, x) for x in values]

    @api.multi
    def write(self, vals):
        if 'name' in vals or 'sequence' in vals:
            vals['to_update'] = True
        return super(PricelistItemGenerator, self).write(vals)

    @api.multi
    def build_pricelist_item(self):
        """ Called by the UI
        """
        prd_list_item_m = self.env['product.pricelist.item']
        for gen in self:
            tmpl_objs = defaultdict(list)
            condition_objs = {}
            # Firstly we are creating missing records
            for item in gen.item_template_ids:
                if item.todo == 'create':
                    tmpl_objs[item] = [x for x in gen.product_condition_ids]
            for condition in gen.product_condition_ids:
                if condition.todo == 'create':
                    condition_objs[condition] = [
                        x for x in gen.item_template_ids
                        if x.todo != 'create']
            for key, val in condition_objs.items():
                for elm in val:
                    tmpl_objs[elm].append(key)
            for tmpl, cond_objs in tmpl_objs.items():
                vals_conditions = gen._get_vals_from_objs(cond_objs)
                tmpl_vals = gen._get_vals_from_objs([tmpl])
                for vals in vals_conditions:
                    values = gen._synchronize_items(tmpl_vals[0], vals)
                    prd_list_item_m.create(values)
            self._unset_todo_create(tmpl_objs, condition_objs)
            # Update all values
            price_items = prd_list_item_m.search(
                [('price_generator_id', '=', gen.id)])
            map_items = {'%s-%s' % (
                         str(x.product_condition_id.id),
                         str(x.item_template_id.id)): x.id
                         for x in price_items}
            tmpl_vals = gen._get_vals_from_objs(gen.item_template_ids)
            condition_vals = gen._get_vals_from_objs(gen.product_condition_ids)
            for tmpl in tmpl_vals:
                for condition in condition_vals:
                    values = gen._synchronize_items(tmpl, condition)
                    p_list_item_id = map_items['%s-%s' % (
                        values.get('product_condition_id'),
                        values.get('item_template_id'))]
                    prd_list_item_m.browse(p_list_item_id).write(values)
            # unset todo
            gen.product_condition_ids.write({'todo': False})
            gen.item_template_ids.write({'todo': False})
            gen.write({'to_update': False})

    @api.model
    def _get_item_generator_fields(self, objects_name):
        if objects_name == 'pricelist.item.template':
            return ['sequence', 'base', 'price_surcharge',
                    'price_discount', 'price_round', 'min_quantity',
                    'price_min_margin', 'price_max_margin']
        else:
            return ['product_id', 'product_tmpl_id', 'categ_id']

    @api.multi
    def _complete_from_generator(self):
        self.ensure_one()
        return {'name': self.name,
                'price_generator_id': self.id,
                'price_version_id': self.price_version_id.id,
                'auto': True}

    @api.multi
    def _unset_todo_create(self, tmpl_objs, condition_objs):
        " Unset todo with 'create' value on both objects "
        self.env['pricelist.item.template'].browse(
            [x.id for x in tmpl_objs.keys()]).write({'todo': False})
        self.env['pricelist.product.condition'].browse(
            [x.id for x in condition_objs.keys()]).write({'todo': False})

    @api.multi
    def _synchronize_items(self, base_vals, vals):
        self.ensure_one()
        values = vals.copy()
        values.update(base_vals)
        values.update(self._complete_from_generator())
        values['sequence'] = ((
            int("{:0<4d}".format(self.sequence)) +
            base_vals['sequence']))
        return values

    @api.multi
    def _get_vals_from_objs(self, objects):
        """ objects: iterable of object records of the models
                    'pricelist.item.template' or 'pricelist.product.condition'
            @return: list of dict of record values
        """
        self.ensure_one()
        values_list = []
        if objects and objects[0]:
            fields = self._get_item_generator_fields(objects[0]._name)
        for object in objects:
            vals = {}
            for field in fields:
                if object[field]:
                    vals[field] = object[field]
                    if field == 'price_discount':
                        # for usability purpose, discount is expressed
                        # in a different way than in 'product.pricelist.item'
                        # here, we convert the field
                        vals[field] = - object[field] / 100
                    if object._fields[field].type == 'many2one':
                        vals[field] = object[field]['id']
            if object._name == 'pricelist.item.template':
                vals['item_template_id'] = object.id
            else:
                vals['product_condition_id'] = object.id
            values_list.append(vals)
        return values_list

    @api.multi
    def activate_generator(self):
        for generator in self:
            if generator.active is False:
                vals = {'active': True, 'to_update': True}
            else:
                vals = {'active': False}
                items_tpl = self.env['pricelist.item.template'].search(
                    [('price_generator_id', '=', generator.id)])
                if items_tpl:
                    items2unlink = self.env['product.pricelist.item'].search([
                        ('item_template_id', 'in', [x.id for x in items_tpl])])
                    if items2unlink:
                        items2unlink.unlink()
                # 'todo' field to initial value
                generator.item_template_ids.write({'todo': 'create'})
                generator.product_condition_ids.write({'todo': 'create'})
            generator.write(vals)
            return True


class PricelistProductCondition(models.Model):
    _name = "pricelist.product.condition"
    _description = "Products selection by criterias"
    _rec_name = 'id'

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product Variant',
        help="If product is selected, no other criterias can be take account")
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template', string='Product',
        help="If product is selected, no other criterias can be take account")
    categ_id = fields.Many2one(
        comodel_name='product.category', string='Category',
        help="Products of the category or products of children categories")
    price_generator_id = fields.Many2one(
        comodel_name='pricelist.item.generator',
        string='Generator', required=True)
    todo = fields.Selection(
        selection=TODO_SELECTION, readonly=True, string='Next Action',
        help="Required action on Pricelist Items")

    @api.model
    def create(self, vals):
        self.env['pricelist.item.generator'].search(
            [('id', '=', vals['price_generator_id'])]).write(
            {'to_update': True})
        vals['todo'] = 'create'
        return super(PricelistProductCondition, self).create(vals)

    @api.multi
    def write(self, vals):
        # Some records shouldn't be written with the same values
        todo_update = update_item_tpl_or_condition(vals, self)
        super(PricelistProductCondition, self).write(vals)
        if todo_update:
            super(PricelistProductCondition, todo_update).write(
                {'todo': 'update'})
        return True


class AbstractPriceListItemGenerator(models.AbstractModel):
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
                _("'Discount' or 'Surcharge' must be different of 0."))

    @api.model
    def _price_field_get(self):
        # TODO future version : support other type of pricelists
        result = []
        result.append((1, _('Public Price')))
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
        self.env['pricelist.item.generator'].search(
            [('id', '=', vals['price_generator_id'])]).write(
            {'to_update': True})
        vals['todo'] = 'create'
        return super(PricelistItemTemplate, self).create(vals)

    @api.multi
    def write(self, vals):
        # Some records shouldn't be written with the same values
        todo_update = update_item_tpl_or_condition(vals, self)
        super(PricelistItemTemplate, self).write(vals)
        if todo_update:
            super(PricelistItemTemplate, todo_update).write(
                {'todo': 'update'})
        return True


class ProductPricelistItem(models.Model):
    _inherit = ['abstract.pricelist.item.generator', 'product.pricelist.item']
    _name = 'product.pricelist.item'

    auto = fields.Boolean(
        string='Auto', default=False,
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
