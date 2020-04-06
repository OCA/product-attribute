# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _name = "product.template"

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu
        )
        if view_type != 'search':  # pragma: no cover
            return res
        else:
            return self.env[
                "product.related.filter.mixin"].add_filter_related_fields(res)


class ProductProduct(models.Model):
    _inherit = "product.product"
    _name = "product.product"

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu
        )
        if view_type != 'search':  # pragma: no cover
            return res
        else:
            return self.env[
                "product.related.filter.mixin"].add_filter_related_fields(res)
