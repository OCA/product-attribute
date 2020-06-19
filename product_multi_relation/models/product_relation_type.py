# Copyright 2013-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
"""Define the type of relations that can exist between products."""
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.osv.expression import AND, OR


HANDLE_INVALID_ONCHANGE = [
    ('restrict',
     _('Do not allow change that will result in invalid relations')),
    ('ignore',
     _('Allow existing relations that do not fit changed conditions')),
    ('end',
     _('End relations per today, if they do not fit changed conditions')),
    ('delete',
     _('Delete relations that do not fit changed conditions')),
]


class ProductRelationType(models.Model):
    """Model that defines relation types that might exist between products"""
    _name = 'product.relation.type'
    _description = 'Product Relation Type'
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )
    name_inverse = fields.Char(
        string='Inverse name',
        required=True,
        translate=True,
    )
    product_type_left = fields.Selection(
        selection='get_product_types',
        string='Left product type',
    )
    product_type_right = fields.Selection(
        selection='get_product_types',
        string='Right product type',
    )
    product_category_left = fields.Many2one(
        comodel_name='product.category',
        string='Left product category',
    )
    product_category_right = fields.Many2one(
        comodel_name='product.category',
        string='Right product category',
    )
    allow_self = fields.Boolean(
        string='Reflexive',
        help='This relation can be set up with the same product left and '
        'right',
        default=False,
    )
    is_symmetric = fields.Boolean(
        string='Symmetric',
        help="This relation is the same from right to left as from left to"
             " right",
        default=False,
    )
    handle_invalid_onchange = fields.Selection(
        selection=HANDLE_INVALID_ONCHANGE,
        string='Invalid relation handling',
        required=True,
        default='restrict',
        help="When adding relations criteria like product type and category"
             " are checked.\n"
             "However when you change the criteria, there might be relations"
             " that do not fit the new criteria.\n"
             "Specify how this situation should be handled.",
    )

    @api.model
    def get_product_types(self):
        """A product can be consumable or an service."""
        return [
            ('consu', _('Consumable')),
            ('service', _('Service')),
        ]

    @api.model
    def _end_active_relations(self, relations):
        """End the relations that are active.

        If a relation is current, that is, if it has a start date
        in the past and end date in the future (or no end date),
        the end date will be set to the current date.

        If a relation has a end date in the past, then it is inactive and
        will not be modified.

        :param relations: a recordset of relations (not necessarily all active)
        """
        today = fields.Date.today()
        for relation in relations:
            if relation.date_start and relation.date_start >= today:
                relation.unlink()

            elif not relation.date_end or relation.date_end > today:
                relation.write({'date_end': today})

    @api.multi
    def check_existing(self, vals):
        """Check wether records exist that do not fit new criteria."""
        relation_model = self.env['product.relation']

        def get_type_condition(vals, side):
            """Add if needed check for product type."""
            fieldname1 = 'product_type_%s' % side
            fieldname2 = '%s_product_id.type' % side
            product_type = fieldname1 in vals and vals[fieldname1] or False
            if product_type:
                # Records that do not have the specified type are invalid:
                return [(fieldname2, 'not in', [product_type])]
            return []

        def get_category_condition(vals, side):
            """Add if needed check for product category."""
            fieldname1 = 'product_category_%s' % side
            fieldname2 = '%s_product_id.categ_id' % side
            category_id = fieldname1 in vals and vals[fieldname1] or False
            if category_id:
                # Records that do not have the specified category are invalid:
                return [(fieldname2, 'not in', [category_id])]
            return []

        last_error = None
        for this in self:
            handling = (
                'handle_invalid_onchange' in vals and
                vals['handle_invalid_onchange'] or
                this.handle_invalid_onchange
            )
            if handling == 'ignore':
                continue
            invalid_conditions = []
            for side in ['left', 'right']:
                invalid_conditions = OR([
                    invalid_conditions,
                    get_type_condition(vals, side),
                ])
                invalid_conditions = OR([
                    invalid_conditions,
                    get_category_condition(vals, side),
                ])
            if not invalid_conditions:
                return
            # only look at relations for this type
            invalid_domain = AND([
                [('type_id', '=', this.id)], invalid_conditions
            ])
            invalid_relations = relation_model.with_context(
                active_test=False
            ).search(invalid_domain)
            if invalid_relations:
                if handling == 'restrict':
                    last_error = ValidationError(
                        _('There are already relations not satisfying the'
                          ' conditions for product type or category.')
                    )
                    break
                elif handling == 'delete':
                    invalid_relations.unlink()
                else:
                    self._end_active_relations(invalid_relations)
        if last_error:
            raise last_error

    def _get_reflexive_relations(self):
        """Get all reflexive relations for this relation type.

        :return: a recordset of product.relation.
        """
        self.env.cr.execute(
            """
            SELECT id FROM product_relation
            WHERE left_product_id = right_product_id
            AND type_id = %(relation_type_id)s
            """, {
                'relation_type_id': self.id,
            }
        )
        reflexive_relation_ids = [r[0] for r in self.env.cr.fetchall()]
        return self.env['product.relation'].browse(reflexive_relation_ids)

    def _check_no_existing_reflexive_relations(self):
        """Check that no reflexive relation exists for these relation types."""
        last_error = None
        for relation_type in self:
            relations = relation_type._get_reflexive_relations()
            if relations:
                last_error = ValidationError(
                    _("Reflexivity could not be disabled for the relation "
                      "type {relation_type}. There are existing reflexive "
                      "relations defined for the following products: "
                      "{products}").format(
                        relation_type=relation_type.display_name,
                        products=relations.mapped(
                            'left_product_id.display_name')))
                break
        if last_error:
            raise last_error

    def _delete_existing_reflexive_relations(self):
        """Delete existing reflexive relations for these relation types."""
        for relation_type in self:
            relations = relation_type._get_reflexive_relations()
            relations.unlink()

    def _end_active_reflexive_relations(self):
        """End active reflexive relations for these relation types."""
        for relation_type in self:
            reflexive_relations = relation_type._get_reflexive_relations()
            self._end_active_relations(reflexive_relations)

    def _handle_deactivation_of_allow_self(self):
        """Handle the deactivation of reflexivity on these relations types."""
        restrict_relation_types = self.filtered(
            lambda t: t.handle_invalid_onchange == 'restrict')
        restrict_relation_types._check_no_existing_reflexive_relations()

        delete_relation_types = self.filtered(
            lambda t: t.handle_invalid_onchange == 'delete')
        delete_relation_types._delete_existing_reflexive_relations()

        end_relation_types = self.filtered(
            lambda t: t.handle_invalid_onchange == 'end')
        end_relation_types._end_active_reflexive_relations()

    @api.multi
    def _update_right_vals(self, vals):
        """Make sure that on symmetric relations, right vals follow left vals.

        @attention: All fields ending in `_right` will have their values
                    replaced by the values of the fields whose names end
                    in `_left`.
        """
        vals['name_inverse'] = vals.get('name', self.name)
        # For all left keys in model, take value for right either from
        # left key in vals, or if not present, from right key in self:
        left_keys = [key for key in self._fields if key.endswith('_left')]
        for left_key in left_keys:
            right_key = left_key.replace('_left', '_right')
            vals[right_key] = vals.get(left_key, self[left_key])
            if hasattr(vals[right_key], 'id'):
                vals[right_key] = vals[right_key].id

    @api.model
    def create(self, vals):
        if vals.get('is_symmetric'):
            self._update_right_vals(vals)
        return super(ProductRelationType, self).create(vals)

    @api.multi
    def write(self, vals):
        """Handle existing relations if conditions change."""
        self.check_existing(vals)

        for rec in self:
            rec_vals = vals.copy()
            if rec_vals.get('is_symmetric', rec.is_symmetric):
                self._update_right_vals(rec_vals)
            super(ProductRelationType, rec).write(rec_vals)

        allow_self_disabled = 'allow_self' in vals and not vals['allow_self']
        if allow_self_disabled:
            self._handle_deactivation_of_allow_self()

        return True

    @api.multi
    def unlink(self):
        """Allow delete of relation type, even when connections exist.

        Relations can be deleted if relation type allows it.
        """
        relation_model = self.env['product.relation']
        types = self.filtered(lambda rec: rec.handle_invalid_onchange == 'delete')
        relations = relation_model.search([('type_id', 'in', types.ids)])
        relations.unlink()
        return super(ProductRelationType, self).unlink()
