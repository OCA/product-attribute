# Copyright 2013-2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# pylint: disable=api-one-deprecated
"""Store relations (connections) between products."""
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductRelation(models.Model):
    """Model product.relation is used to describe all links or relations
    between products in the database.

    This model is actually only used to store the data. The model
    product.relation.all, based on a view that contains each record
    two times, once for the normal relation, once for the inverse relation,
    will be used to maintain the data.
    """
    _name = 'product.relation'
    _description = 'Product relation'

    left_product_id = fields.Many2one(
        comodel_name='product.template',
        string='Source Product',
        required=True,
        auto_join=True,
        ondelete='cascade',
    )
    right_product_id = fields.Many2one(
        comodel_name='product.template',
        string='Destination Product',
        required=True,
        auto_join=True,
        ondelete='cascade',
    )
    type_id = fields.Many2one(
        comodel_name='product.relation.type',
        string='Type',
        required=True,
        auto_join=True,
    )
    date_start = fields.Date('Starting date')
    date_end = fields.Date('Ending date')

    @api.model
    def create(self, vals):
        """Override create to correct values, before being stored."""
        context = self.env.context
        if 'left_product_id' not in vals and context.get('active_id'):
            vals['left_product_id'] = context.get('active_id')
        return super(ProductRelation, self).create(vals)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        """End date should not be before start date, if not filled

        :raises ValidationError: When constraint is violated
        """
        for record in self:
            if (record.date_start and record.date_end and
                    record.date_start > record.date_end):
                raise ValidationError(
                    _('The starting date cannot be after the ending date.')
                )

    @api.constrains('left_product_id', 'type_id')
    def _check_product_left(self):
        """Check left product for required product

        :raises ValidationError: When constraint is violated
        """
        self._check_product("left")

    @api.constrains('right_product_id', 'type_id')
    def _check_product_right(self):
        """Check right product for required product

        :raises ValidationError: When constraint is violated
        """
        self._check_product("right")

    @api.multi
    def _check_product(self, side):
        """Check product for required product, and for category

        :param str side: left or right
        :raises ValidationError: When constraint is violated
        """
        for record in self:
            assert side in ['left', 'right']
            ptype = getattr(record.type_id, "product_type_%s" % side)
            product = getattr(record, '%s_product_id' % side)
            if ptype and ptype != product.type:
                raise ValidationError(
                    _('The %s product is not applicable for this '
                      'relation type.') % side
                )
            category = getattr(record.type_id, "product_category_%s" % side)
            if category and category.id not in product.categ_id.ids:
                raise ValidationError(
                    _('The %s product does not have category %s.') %
                    (side, category.name)
                )

    @api.constrains('left_product_id', 'right_product_id')
    def _check_not_with_self(self):
        """Not allowed to link product to same product

        :raises ValidationError: When constraint is violated
        """
        for record in self:
            if record.left_product_id == record.right_product_id:
                if not (record.type_id and record.type_id.allow_self):
                    raise ValidationError(
                        _('Products cannot have a relation with themselves.')
                    )

    @api.constrains(
        'left_product_id',
        'type_id',
        'right_product_id',
        'date_start',
        'date_end',
    )
    def _check_relation_uniqueness(self):
        """Forbid multiple active relations of the same type between the same
        products

        :raises ValidationError: When constraint is violated
        """
        # pylint: disable=no-member
        # pylint: disable=no-value-for-parameter
        for record in self:
            domain = [
                ('type_id', '=', record.type_id.id),
                ('id', '!=', record.id),
                ('left_product_id', '=', record.left_product_id.id),
                ('right_product_id', '=', record.right_product_id.id),
            ]
            if record.date_start:
                domain += [
                    '|',
                    ('date_end', '=', False),
                    ('date_end', '>=', record.date_start),
                ]
            if record.date_end:
                domain += [
                    '|',
                    ('date_start', '=', False),
                    ('date_start', '<=', record.date_end),
                ]
            if record.search(domain):
                raise ValidationError(
                    _('There is already a similar relation with '
                      'overlapping dates')
                )
