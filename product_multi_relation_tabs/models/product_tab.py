# Copyright 2017-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from ..tablib import Tab


class ResProductTab(models.Model):
    """Model that defines relation types that might exist between products"""
    _name = 'product.tab'
    _description = 'Tabs to add to product'
    _order = 'name'

    @api.model
    def get_product_types(self):
        """Product types are defined by model product.relation.type."""
        # pylint: disable=no-self-use
        rprt_model = self.env['product.relation.type']
        return rprt_model.get_product_types()

    code = fields.Char(
        string='Code',
        required=True,
        help="Language independent code for tab")
    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
        help="Will provide title for tab in user language")
    product_type = fields.Selection(
        selection='get_product_types',
        string='Valid for product type')
    product_category_id = fields.Many2one(
        comodel_name='product.category',
        string='Valid for product category')
    product_ids = fields.Many2many(
        comodel_name='product.template',
        string="Products with this tab",
        help="This tab will only show for certain products.\n"
             "Do not combine this with selection for product type or"
             " category.")

    @api.constrains('product_type', 'product_category_id', 'product_ids')
    def _check_product_ids(self):
        """If product_ids filled, other domain fields should be empty."""
        if self.product_ids and \
                (self.product_type or self.product_category_id):
            raise ValidationError(_(
                "You can not both specify product_ids and other criteria."))

    @api.multi
    def update_types(self, vals=None):
        """Update types on write or unlink.

        If we have no vals, assume unlink.
        """
        if vals:
            product_type = vals.get('product_type', False)
            product_category_id = vals.get('product_category_id', False)
        type_model = self.env['product.relation.type']
        for this in self:
            for tab_side in ('left', 'right'):
                side_tab = 'tab_%s_id' % tab_side
                tab_using = type_model.search([(side_tab, '=', this.id)])
                for relation_type in tab_using:
                    type_value = relation_type['product_type_%s' % tab_side]
                    category_value = \
                        relation_type['product_category_%s' % tab_side]
                    if (not vals or
                            (product_type and product_type != type_value) or
                            (product_category_id and
                             product_category_id != category_value.id)):
                        relation_type.write({side_tab: False})

    @api.multi
    def write(self, vals):
        """Remove tab from types no longer satifying criteria."""
        if vals.get('product_type', False) or \
                vals.get('product_category_id', False):
            self.update_types(vals)
        result = super(ResProductTab, self).write(vals)
        return result

    @api.multi
    def unlink(self):
        """Unlink should first remove references."""
        self.update_types()
        return super(ResProductTab, self).unlink()

    @api.model
    def get_tabs(self):
        """Convert information on tabs in database to array of objects."""
        tabs = [Tab(tab_record) for tab_record in self.search([])]
        return tabs
