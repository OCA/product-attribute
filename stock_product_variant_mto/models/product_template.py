# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, values):
        mto_route = self.env.ref("stock.route_warehouse0_mto", raise_if_not_found=False)

        if "route_ids" not in values or not mto_route:
            return super().write(values)

        # As _compute_is_mto cannot use api.depends (or it would reset MTO
        # route on variants as soon as there is a change on the template routes),
        # we need to check which template in self had MTO route activated
        # or deactivated to force the recomputation of is_mto on variants

        templates_not_mto_before = self.filtered(lambda t: mto_route not in t.route_ids)

        res = super().write(values)

        templates_mto_after = self.filtered(lambda t: mto_route in t.route_ids)
        templates_mto_added = templates_not_mto_before & templates_mto_after
        templates_mto_removed = self - templates_mto_after - templates_not_mto_before

        (
            templates_mto_added | templates_mto_removed
        ).product_variant_ids._compute_is_mto()

        return res

    @api.onchange("route_ids")
    def onchange_route_ids(self):
        mto_route = self.env.ref("stock.route_warehouse0_mto", raise_if_not_found=False)
        if not mto_route:
            return

        origin_routes = (
            self._origin.route_ids if self._origin else self.env["stock.route"]
        )
        current_routes = (
            self.route_ids._origin if self.route_ids else self.env["stock.route"]
        )

        if mto_route not in origin_routes and mto_route in current_routes:
            # Return warning activating MTO route
            return {
                "warning": {
                    "title": self.env._("Warning"),
                    "message": self.env._(
                        "Activating MTO route will reset `Variant is MTO` "
                        "setting on the variants."
                    ),
                }
            }

        if mto_route in origin_routes and mto_route not in current_routes:
            # Return warning deactivating MTO route
            return {
                "warning": {
                    "title": self.env._("Warning"),
                    "message": self.env._(
                        "Deactivating MTO route will reset `Variant is MTO` "
                        "setting on the variants."
                    ),
                }
            }
