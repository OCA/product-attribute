# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    product_brand_id = fields.Many2one(
        comodel_name='product.brand',
        string='Brand',
    )

    # pylint:disable=dangerous-default-value
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        query_str = super()._query(
            with_clause=with_clause, fields=fields, groupby=groupby,
            from_clause=from_clause)
        # Split query
        with_clause, following = query_str.split('SELECT')
        select_clause, following = following.split('FROM')
        from_clause, following = following.split('WHERE')
        where_clause, following = following.split('GROUP BY')
        groupby_clause = following.split(')')[0]
        # Add in query
        select_clause += """, t.product_brand_id"""
        groupby_clause += ", t.product_brand_id"
        # Recompose query
        res = ("SELECT {select_clause} "
               "FROM {from_clause} "
               "WHERE {where_clause} "
               "GROUP BY {groupby_clause}".format(**locals()))
        return res
