# Copyright 2014-2018 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import collections
import logging

from psycopg2.extensions import AsIs

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import drop_view_if_exists


_logger = logging.getLogger(__name__)


# Register relations
RELATIONS_SQL = """\
SELECT
    (rel.id * %%(padding)s) + %(key_offset)s AS id,
    'product.relation' AS res_model,
    rel.id AS res_id,
    rel.left_product_id AS this_product_id,
    rel.right_product_id AS other_product_id,
    rel.type_id,
    rel.date_start,
    rel.date_end,
    %(is_inverse)s as is_inverse
    %(extra_additional_columns)s
FROM product_relation rel"""

# Register inverse relations
RELATIONS_SQL_INVERSE = """\
SELECT
    (rel.id * %%(padding)s) + %(key_offset)s AS id,
    'product.relation',
    rel.id,
    rel.right_product_id,
    rel.left_product_id,
    rel.type_id,
    rel.date_start,
    rel.date_end,
    %(is_inverse)s as is_inverse
    %(extra_additional_columns)s
FROM product_relation rel"""


class ProductRelationAll(models.AbstractModel):
    """Abstract model to show each relation from two sides."""
    _auto = False
    _log_access = False
    _name = 'product.relation.all'
    _description = 'All (non-inverse + inverse) relations between products'
    _order = \
        'this_product_id, type_selection_id, date_end desc, date_start desc'

    res_model = fields.Char(
        string='Resource Model',
        readonly=True,
        required=True,
        help="The database object this relation is based on.")
    res_id = fields.Integer(
        string='Resource ID',
        readonly=True,
        required=True,
        help="The id of the object in the model this relation is based on.")
    this_product_id = fields.Many2one(
        comodel_name='product.template',
        string='One Product',
        required=True)
    other_product_id = fields.Many2one(
        comodel_name='product.template',
        string='Other Product',
        required=True)
    type_id = fields.Many2one(
        comodel_name='product.relation.type',
        string='Underlying Relation Type',
        readonly=True,
        required=True)
    date_start = fields.Date('Starting date')
    date_end = fields.Date('Ending date')
    is_inverse = fields.Boolean(
        string="Is reverse type?",
        readonly=True,
        help="Inverse relations are from right to left product.")
    type_selection_id = fields.Many2one(
        comodel_name='product.relation.type.selection',
        string='Relation Type',
        required=True)
    active = fields.Boolean(
        string='Active',
        readonly=True,
        help="Records with date_end in the past are inactive")
    any_product_id = fields.Many2many(
        comodel_name='product.template',
        string='Product',
        compute=lambda self: None,
        search='_search_any_product_id')

    def register_specification(
            self, register, base_name, is_inverse, select_sql):
        _last_key_offset = register['_lastkey']
        key_name = base_name + (is_inverse and '_inverse' or '')
        if key_name in register:
            raise ValidationError(_('"%s" in "%s"') % (key_name, register))
        if '%%(padding)s' not in select_sql:
            raise ValidationError(_('"%s" not in "%s"') % ('%%(padding)s', select_sql))
        if '%(key_offset)s' not in select_sql:
            raise ValidationError(_('"%s" in "%s"') % ('%(key_offset)s', select_sql))
        if '%(is_inverse)s' not in select_sql:
            raise ValidationError(_('"%s" in "%s"') % ('%(is_inverse)s', select_sql))
        _last_key_offset += 1
        register['_lastkey'] = _last_key_offset
        register[key_name] = dict(
            base_name=base_name,
            is_inverse=is_inverse,
            key_offset=_last_key_offset,
            select_sql=select_sql % {
                'key_offset': _last_key_offset,
                'is_inverse': is_inverse,
                'extra_additional_columns':
                self._get_additional_relation_columns(),
            })

    def get_register(self):
        register = collections.OrderedDict()
        register['_lastkey'] = -1
        self.register_specification(
            register, 'relation', False, RELATIONS_SQL)
        self.register_specification(
            register, 'relation', True, RELATIONS_SQL_INVERSE)
        return register

    def get_select_specification(self, base_name, is_inverse):
        register = self.get_register()
        key_name = base_name + (is_inverse and '_inverse' or '')
        return register[key_name]

    def _get_statement(self):
        """Allow other modules to add to statement."""
        register = self.get_register()
        union_select = ' UNION '.join(
            [register[key]['select_sql']
             for key in register if key != '_lastkey'])
        return """\
CREATE OR REPLACE VIEW %%(table)s AS
     WITH base_selection AS (%(union_select)s)
 SELECT
     bas.*,
     CASE
         WHEN NOT bas.is_inverse OR typ.is_symmetric
         THEN bas.type_id * 2
         ELSE (bas.type_id * 2) + 1
     END as type_selection_id,
     (bas.date_end IS NULL OR bas.date_end >= current_date) AS active
     %%(additional_view_fields)s
 FROM base_selection bas
 JOIN product_relation_type typ ON (bas.type_id = typ.id)
 %%(additional_tables)s
        """ % {'union_select': union_select}

    def _get_padding(self):
        """Utility function to define padding in one place."""
        return 100

    def _get_additional_relation_columns(self):
        """Get additionnal columns from product_relation.

        This allows to add fields to the model product.relation
        and display these fields in the product.relation.all list view.

        :return: ', rel.column_a, rel.column_b_id'
        """
        return ''

    def _get_additional_view_fields(self):
        """Allow inherit models to add fields to view.

        If fields are added, the resulting string must have each field
        prepended by a comma, like so:
            return ', typ.allow_self, typ.left_product_category'
        """
        return ''

    def _get_additional_tables(self):
        """Allow inherit models to add tables (JOIN's) to view.

        Example:
            return 'JOIN type_extention ext ON (bas.type_id = ext.id)'
        """
        return ''

    @api.model_cr_context
    def _auto_init(self):
        cr = self._cr
        drop_view_if_exists(cr, self._table)
        cr.execute(
            self._get_statement(),
            {'table': AsIs(self._table),
             'padding': self._get_padding(),
             'additional_view_fields':
                AsIs(self._get_additional_view_fields()),
             'additional_tables':
                AsIs(self._get_additional_tables())})
        return super(ProductRelationAll, self)._auto_init()

    @api.model
    def _search_any_product_id(self, operator, value):
        """Search relation with product, no matter on which side."""
        return [
            '|',
            ('this_product_id', operator, value),
            ('other_product_id', operator, value)]

    @api.multi
    def name_get(self):
        return {
            this.id: '%s %s %s' % (
                this.this_product_id.name,
                this.type_selection_id.display_name,
                this.other_product_id.name,
            ) for this in self}

    def _check_product_domain(self, product, product_domain, side):
        """Check wether product_domain results in empty selection
        for product, or wrong selection of product already selected.
        """
        warning = {}
        if product:
            test_domain = [('id', '=', product.id)] + product_domain
        else:
            test_domain = product_domain
        product_model = self.env['product.template']
        products_found = product_model.search(test_domain, limit=1)
        if not products_found:
            warning['title'] = _('Error!')
            if product:
                warning['message'] = (
                    _('%s product incompatible with relation type.') %
                    side.title())
            else:
                warning['message'] = (
                    _('No %s product available for relation type.') %
                    side)
        return warning

    @api.onchange('type_selection_id')
    def onchange_type_selection_id(self):
        """Add domain on products according to category and product_type."""

        this_product_domain = []
        other_product_domain = []
        if self.type_selection_id.product_type_this:
            this_product_domain.append((
                'type', '=',
                self.type_selection_id.product_type_this))
        if self.type_selection_id.product_category_this:
            this_product_domain.append((
                'categ_id', '=',
                self.type_selection_id.product_category_this.id))
        if self.type_selection_id.product_type_other:
            other_product_domain.append((
                'type', '=',
                self.type_selection_id.product_type_other))
        if self.type_selection_id.product_category_other:
            other_product_domain.append((
                'categ_id', '=',
                self.type_selection_id.product_category_other.id))
        result = {'domain': {
            'this_product_id': this_product_domain,
            'other_product_id': other_product_domain}}
        # Check wether domain results in no choice or wrong choice of products:
        warning = {}
        product_model = self.env['product.template']
        if this_product_domain:
            this_product = False
            if self.this_product_id.id:
                this_product = self.this_product_id
            else:
                this_product_id = \
                    'default_this_product_id' in self.env.context and \
                    self.env.context['default_this_product_id'] or \
                    'active_id' in self.env.context and \
                    self.env.context['active_id'] or \
                    False
                if this_product_id:
                    this_product = product_model.browse(this_product_id)
            warning = self._check_product_domain(
                this_product, this_product_domain, _('this'))
        if not warning and other_product_domain:
            warning = self._check_product_domain(
                self.other_product_id, other_product_domain, _('other'))
        if warning:
            result['warning'] = warning
        return result

    def _check_type_selection_domain(self, type_selection_domain):
        """If type_selection_id already selected, check wether it
        is compatible with the computed type_selection_domain. An empty
        selection can practically only occur in a practically empty
        database, and will not lead to problems. Therefore not tested.
        """
        warning = {}
        if not (type_selection_domain and self.type_selection_id):
            return warning
        test_domain = (
            [('id', '=', self.type_selection_id.id)] +
            type_selection_domain)
        type_model = self.env['product.relation.type.selection']
        types_found = type_model.search(test_domain, limit=1)
        if not types_found:
            warning['title'] = _('Error!')
            warning['message'] = _(
                'Relation type incompatible with selected product(s).')
        return warning

    @api.onchange(
        'this_product_id',
        'other_product_id')
    def onchange_product_id(self):
        """Set domain on type_selection_id based on product(s) selected."""

        type_selection_domain = []
        if self.this_product_id:
            type_selection_domain += [
                '|',
                ('product_type_this', '=', False),
                ('product_type_this', '=',
                 self.this_product_id.type),
                '|',
                ('product_category_this', '=', False),
                ('product_category_this', '=',
                 self.this_product_id.categ_id.id)]
        if self.other_product_id:
            type_selection_domain += [
                '|',
                ('product_type_other', '=', False),
                ('product_type_other', '=',
                 self.other_product_id.type),
                '|',
                ('product_category_other', '=', False),
                ('product_category_other', '=',
                 self.other_product_id.categ_id.id)]
        result = {'domain': {
            'type_selection_id': type_selection_domain}}
        # Check wether domain results in no choice or wrong choice for
        # type_selection_id:
        warning = self._check_type_selection_domain(type_selection_domain)
        if warning:
            result['warning'] = warning
        return result

    @api.model
    def _correct_vals(self, vals, type_selection):
        """Fill left and right product from this and other product."""
        vals = vals.copy()
        if 'type_selection_id' in vals:
            vals['type_id'] = type_selection.type_id.id
        if type_selection.is_inverse:
            if 'this_product_id' in vals:
                vals['right_product_id'] = vals['this_product_id']
            if 'other_product_id' in vals:
                vals['left_product_id'] = vals['other_product_id']
        else:
            if 'this_product_id' in vals:
                vals['left_product_id'] = vals['this_product_id']
            if 'other_product_id' in vals:
                vals['right_product_id'] = vals['other_product_id']
        # Delete values not in underlying table:
        for key in (
                'this_product_id',
                'type_selection_id',
                'other_product_id',
                'is_inverse'):
            if key in vals:
                del vals[key]
        return vals

    @api.multi
    def get_base_resource(self):
        """Get base resource from res_model and res_id."""
        self.ensure_one()
        base_model = self.env[self.res_model]
        return base_model.browse([self.res_id])

    @api.multi
    def write_resource(self, base_resource, vals):
        """write handled by base resource."""
        self.ensure_one()
        # write for models other then product.relation SHOULD
        # be handled in inherited models:
        relation_model = self.env['product.relation']
        if self.res_model != relation_model._name:
            raise ValidationError(_('"%s" != "%s"') % (self.res_model, relation_model._name))
        base_resource.write(vals)

    @api.model
    def _get_type_selection_from_vals(self, vals):
        """Get type_selection_id straight from vals or compute from type_id.
        """
        type_selection_id = vals.get('type_selection_id', False)
        if not type_selection_id:
            type_id = vals.get('type_id', False)
            if type_id:
                is_inverse = vals.get('is_inverse')
                type_selection_id = type_id * 2 + (is_inverse and 1 or 0)
        return type_selection_id and self.type_selection_id.browse(
            type_selection_id) or False

    @api.multi
    def write(self, vals):
        """For model 'product.relation' call write on underlying model.
        """
        new_type_selection = self._get_type_selection_from_vals(vals)
        for rec in self:
            type_selection = new_type_selection or rec.type_selection_id
            vals = rec._correct_vals(vals, type_selection)
            base_resource = rec.get_base_resource()
            rec.write_resource(base_resource, vals)
        # Invalidate cache to make product.relation.all reflect changes
        # in underlying product.relation:
        self.env.clear()
        return True

    @api.model
    def _compute_base_name(self, type_selection):
        """This will be overridden for each inherit model."""
        return 'relation'

    @api.model
    def _compute_id(self, base_resource, type_selection):
        """Compute id. Allow for enhancements in inherit model."""
        base_name = self._compute_base_name(type_selection)
        key_offset = self.get_select_specification(
            base_name, type_selection.is_inverse)['key_offset']
        return base_resource.id * self._get_padding() + key_offset

    @api.model
    def create_resource(self, vals, type_selection):
        relation_model = self.env['product.relation']
        return relation_model.create(vals)

    @api.model
    def create(self, vals):
        """Divert non-problematic creates to underlying table.

        Create a product.relation but return the converted id.
        """
        type_selection = self._get_type_selection_from_vals(vals)
        if not type_selection:  # Should not happen
            raise ValidationError(
                _('No relation type specified in vals: %s.') % vals)
        vals = self._correct_vals(vals, type_selection)
        base_resource = self.create_resource(vals, type_selection)
        res_id = self._compute_id(base_resource, type_selection)
        return self.browse(res_id)

    @api.multi
    def unlink_resource(self, base_resource):
        """Delegate unlink to underlying model."""
        self.ensure_one()
        # unlink for models other then product.relation SHOULD
        # be handled in inherited models:
        relation_model = self.env['product.relation']
        if self.res_model != relation_model._name:
            raise ValidationError(_('"%s" != "%s"') % (self.res_model, relation_model._name))
        base_resource.unlink()

    @api.multi
    def unlink(self):
        """For model 'product.relation' call unlink on underlying model.
        """
        for rec in self:
            base_resource = rec.get_base_resource()
            rec.unlink_resource(base_resource)
        return True
