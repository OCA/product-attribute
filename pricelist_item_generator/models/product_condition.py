# coding: utf-8
# © 2016 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


TODO_SELECTION = [('update', 'Update'), ('create', 'Create')]


def update_item_tpl_or_condition(self, vals):
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
        todo_update = update_item_tpl_or_condition(self, vals)
        super(PricelistProductCondition, self).write(vals)
        if todo_update:
            super(PricelistProductCondition, todo_update).write(
                {'todo': 'update'})
        return True
