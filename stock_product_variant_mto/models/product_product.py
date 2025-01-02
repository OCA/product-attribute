# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models

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
        store=False,
        domain="[('product_selectable', '=', True)]",
        search="_search_route_ids",
    )

    def _compute_is_mto(self):
        mto_route = self.env.ref("stock.route_warehouse0_mto", raise_if_not_found=False)
        if not mto_route:
            self.update({"is_mto": False})
            return

        for product in self:
            product.is_mto = mto_route in product.product_tmpl_id.route_ids

    @api.depends("is_mto", "product_tmpl_id.route_ids")
    def _compute_route_ids(self):
        mto_route = self.env.ref("stock.route_warehouse0_mto", raise_if_not_found=False)
        for product in self:
            template_routes = product.product_tmpl_id.route_ids

            if mto_route:
                if product.is_mto and mto_route not in template_routes:
                    template_routes += mto_route
                elif not product.is_mto and mto_route in template_routes:
                    template_routes -= mto_route

            product.route_ids = template_routes

    def _search_route_ids(self, operator, value):
        mto_route = self.env.ref("stock.route_warehouse0_mto", raise_if_not_found=False)
        if not mto_route:
            return [(0, "=", 1)] if operator in ("=", "in") else [(0, "=", 0)]

        if (operator, value) in [("=", mto_route.id), ("in", [mto_route.id])]:
            return [
                ("product_tmpl_id.route_ids", operator, value),
                ("is_mto", "=", True),
            ]
        elif operator in ("!=", "not in") and mto_route.id in value:
            return [
                "|",
                ("product_tmpl_id.route_ids", operator, value),
                ("is_mto", "=", False),
            ]
        return [("product_tmpl_id.route_ids", operator, value)]
