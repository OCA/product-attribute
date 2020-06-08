# Copyright 2013-2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Support connections between products."""
import numbers

from odoo import _, api, exceptions, fields, models
from odoo.osv.expression import is_leaf, OR, FALSE_LEAF


class ProductTemplate(models.Model):
    """Extend product with relations and allow to search for relations
    in various ways.
    """
    _inherit = 'product.template'

    relation_count = fields.Integer(
        string='Relation Count',
        compute="_compute_relation_count"
    )
    relation_all_ids = fields.One2many(
        comodel_name='product.relation.all',
        inverse_name='this_product_id',
        string='All relations with current product',
        auto_join=True,
        selectable=False,
        copy=False,
    )
    search_relation_type_id = fields.Many2one(
        comodel_name='product.relation.type.selection',
        compute=lambda self: None,
        search='_search_relation_type_id',
        string='Has relation of type',
    )
    search_relation_product_id = fields.Many2one(
        comodel_name='product.template',
        compute=lambda self: None,
        search='_search_related_product_id',
        string='Has relation with',
    )
    search_relation_date = fields.Date(
        compute=lambda self: None,
        search='_search_relation_date',
        string='Relation valid',
    )
    search_relation_product_categ_id = fields.Many2one(
        comodel_name='product.category',
        compute=lambda self: None,
        search='_search_related_product_category_id',
        string='Has relation with a product in category',
    )

    @api.depends("relation_all_ids")
    def _compute_relation_count(self):
        """Count the number of relations this product has for Smart Button

        Don't count inactive relations.
        """
        for rec in self:
            rec.relation_count = len(rec.relation_all_ids.filtered('active'))

    @api.model
    def _search_relation_type_id(self, operator, value):
        """Search products based on their type of relations."""
        result = []
        SUPPORTED_OPERATORS = (
            '=',
            '!=',
            'like',
            'not like',
            'ilike',
            'not ilike',
            'in',
            'not in',
        )
        if operator not in SUPPORTED_OPERATORS:
            raise exceptions.ValidationError(
                _('Unsupported search operator "%s"') % operator)
        type_selection_model = self.env['product.relation.type.selection']
        relation_type_selection = []
        if operator == '=' and isinstance(value, numbers.Integral):
            relation_type_selection += type_selection_model.browse(value)
        elif operator == '!=' and isinstance(value, numbers.Integral):
            relation_type_selection = type_selection_model.search([
                ('id', operator, value),
            ])
        else:
            relation_type_selection = type_selection_model.search([
                '|',
                ('type_id.name', operator, value),
                ('type_id.name_inverse', operator, value),
            ])
        if not relation_type_selection:
            result = [FALSE_LEAF]
        for relation_type in relation_type_selection:
            result = OR([
                result,
                [
                    ('relation_all_ids.type_selection_id.id', '=',
                     relation_type.id),
                ],
            ])
        return result

    @api.model
    def _search_related_product_id(self, operator, value):
        """Find product based on relation with other product."""
        return [
            ('relation_all_ids.other_product_id', operator, value),
        ]

    @api.model
    def _search_relation_date(self, operator, value):
        """Look only for relations valid at date of search."""
        return [
            '&',
            '|',
            ('relation_all_ids.date_start', '=', False),
            ('relation_all_ids.date_start', '<=', value),
            '|',
            ('relation_all_ids.date_end', '=', False),
            ('relation_all_ids.date_end', '>=', value),
        ]

    @api.model
    def _search_related_product_category_id(self, operator, value):
        """Search for product related to a product with search category."""
        return [
            ('relation_all_ids.other_product_id.categ_id', operator, value),
        ]

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """Inject searching for current relation date if we search for
        relation properties and no explicit date was given.
        """
        date_args = []
        for arg in args:
            if (is_leaf(arg) and isinstance(arg[0], str) and
                    arg[0].startswith('search_relation')):
                if arg[0] == 'search_relation_date':
                    date_args = []
                    break
                if not date_args:
                    date_args = [
                        ('search_relation_date', '=', fields.Date.today()),
                    ]
        # because of auto_join, we have to do the active test by hand
        active_args = []
        if self.env.context.get('active_test', True):
            for arg in args:
                if (is_leaf(arg) and isinstance(arg[0], str) and
                        arg[0].startswith('search_relation')):
                    active_args = [('relation_all_ids.active', '=', True)]
                    break
        return super(ProductTemplate, self).search(
            args + date_args + active_args, offset=offset, limit=limit,
            order=order, count=count)
