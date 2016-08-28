# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api
from collections import defaultdict


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
        string='Active', copy=False,
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
        return super(PricelistItemGenerator, self).copy(default=default)

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
                    condition_objs[condition] = gen.item_template_ids.filtered(
                        lambda x: x.todo != 'create')
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
            # Then we update all values
            price_items = prd_list_item_m.search(
                [('price_generator_id', '=', gen.id)])
            map_items = {'%s-%s' % (
                         x.product_condition_id.id,
                         x.item_template_id.id): x.id
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
            gen.write({
                'to_update': False,
                # unset todo
                'product_condition_ids': [
                    (1, r.id, {'todo': False})
                    for r in gen.product_condition_ids],
                'item_template_ids': [
                    (1, r.id, {'todo': False})
                    for r in gen.item_template_ids],
            })

    @api.model
    def _get_item_generator_fields(self, objects_name):
        if objects_name == 'pricelist.item.template':
            return ['sequence', 'base', 'base_pricelist_id', 'price_surcharge',
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
            vals.update({
                'product_condition_ids': [
                    # 'todo' field to initial value
                    (1, r.id, {'todo': 'create'})
                    for r in generator.product_condition_ids],
                'item_template_ids': [
                    (1, r.id, {'todo': 'create'})
                    for r in generator.item_template_ids],
            })
            generator.write(vals)
            return True
