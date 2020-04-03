# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResProductRelationAll(models.AbstractModel):
    """Abstract model to show each relation from two sides."""
    _inherit = 'product.relation.all'

    tab_id = fields.Many2one(
        comodel_name='product.tab',
        string='Show relation on tab',
        readonly=True,
    )

    def _get_additional_view_fields(self):
        """Add tab_id to view fields."""
        # pylint: disable=no-member
        return ','.join([
            super(ResProductRelationAll, self)._get_additional_view_fields(),
            "CASE"
            "    WHEN NOT bas.is_inverse"
            "    THEN lefttab.id"
            "    ELSE righttab.id"
            " END as tab_id"])

    def _get_additional_tables(self):
        """Add product_tab table to view."""
        # pylint: disable=no-member
        return ' '.join([
            super(ResProductRelationAll, self)._get_additional_tables(),
            "LEFT OUTER JOIN product_tab lefttab"
            " ON typ.tab_id_left = lefttab.id",
            "LEFT OUTER JOIN product_tab righttab"
            " ON typ.tab_id_right = righttab.id"])

    @api.onchange(
        'this_product_id',
        'other_product_id',
    )
    def onchange_product_id(self):
        """Add tab if needed to type_selection_id domain.

        This method makes sure that when a relation is added to a tab,
        it is with a relation type meant to be placed on that tab.
        """
        # pylint: disable=no-member
        result = super(ResProductRelationAll, self).onchange_product_id()
        if 'default_tab_id' in self.env.context:
            result['domain'] = result['domain'] if 'domain' in result else {}
            result['domain']['type_selection_id'] = \
                result['domain']['type_selection_id'] \
                if 'type_selection_id' in result['domain'] else {}
            result['domain']['type_selection_id'].append(
                ('tab_id', '=', self.env.context['default_tab_id']))
        return result
