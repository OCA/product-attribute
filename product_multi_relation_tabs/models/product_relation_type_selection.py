# Copyright 2013-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResProductRelationTypeSelection(models.Model):
    """Virtual relation types"""
    _inherit = 'product.relation.type.selection'

    tab_id = fields.Many2one(
        comodel_name='product.tab',
        string='Show relation on tab',
        readonly=True,
    )

    def _get_additional_view_fields(self):
        """Add tab_id to fields in view."""
        return ','.join([
            super(ResProductRelationTypeSelection, self)
            ._get_additional_view_fields(),
            "CASE"
            "    WHEN NOT bas.is_inverse"
            "    THEN lefttab.id"
            "    ELSE righttab.id"
            " END as tab_id"])

    def _get_additional_tables(self):
        """Add two links to product_tab."""
        return ' '.join([
            super(ResProductRelationTypeSelection, self)
            ._get_additional_tables(),
            "LEFT OUTER JOIN product_tab lefttab"
            " ON typ.tab_left_id = lefttab.id",
            "LEFT OUTER JOIN product_tab righttab"
            " ON typ.tab_right_id = righttab.id"])
