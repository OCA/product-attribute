# Copyright 2023 Camptocamp SA
# Copyright 2025 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models
from odoo.exceptions import ValidationError

IS_MTO_HELP = """
    Check or Uncheck this field to enable the Make To Order on the variant,
    independantly from its template configuration.\n
    Please note that activating or deactivating Make To Order on the template,
    will reset this setting on its variants.
"""


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_mto = fields.Boolean(
        string="Variant is MTO",
        compute="_compute_is_mto",
        store=True,
        readonly=False,
        help=IS_MTO_HELP,
    )

    route_ids = fields.Many2many(
        "stock.route",
        compute="_compute_route_ids",
        domain="[('product_selectable', '=', True)]",
        store=False,
        search="_search_route_ids",
        inverse="_inverse_route_ids",
    )

    def _compute_is_mto(self):
        for product in self:
            product.is_mto = product.product_tmpl_id.is_mto

    @api.depends("is_mto", "product_tmpl_id.route_ids")
    def _compute_route_ids(self):
        mto_routes = self.env["stock.route"].search([("is_mto", "=", True)])
        for product in self:
            routes = product.product_tmpl_id.route_ids
            if product.is_mto:
                routes += mto_routes
            product.route_ids = routes

    def _search_route_ids(self, operator, value):
        mto_routes = self.env["stock.route"].search([("is_mto", "=", True)])
        if operator in ("=", "!=") and value in mto_routes:
            return [("is_mto", operator, True)]
        domain = []
        route_ids = value.copy()
        for idx, route_id in enumerate(route_ids):
            if route_id in mto_routes.ids:
                route_ids.pop(idx)
                domain = [("is_mto", "=" if operator == "in" else "!=", True)]
        if route_ids:
            domain += [("product_tmpl_id.route_ids", operator, route_ids)]
        return domain

    def _inverse_route_ids(self):
        mto_routes = self.env["stock.route"].search([("is_mto", "=", True)])
        for product in self:
            non_mto_routes = product.route_ids - mto_routes
            if product.route_ids & mto_routes:
                if not product.is_mto:
                    product.is_mto = True
            else:
                if product.is_mto:
                    product.is_mto = False
            if product.product_tmpl_id.route_ids != non_mto_routes:
                product.product_tmpl_id.route_ids = non_mto_routes

    @api.constrains("is_mto")
    def _check_template_is_mto(self):
        for product in self:
            if not product.is_mto and product.product_tmpl_id.is_mto:
                raise ValidationError(
                    self.env._(
                        "You cannot mark a variant as non MTO when the product is MTO"
                    )
                )
