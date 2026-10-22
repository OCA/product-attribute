# Copyright 2023 Camptocamp SA
# Copyright 2025 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, values):
        if "route_ids" not in values:
            return super().write(values)

        # As _compute_is_mto cannot use api.depends (or it would reset MTO
        # route on variants as soon as there is a change on the template routes),
        # we need to check which template in self had MTO route activated
        # or deactivated to force the recomputation of is_mto on variants
        templates_mto_before = self.filtered("is_mto")
        templates_not_mto_before = self - templates_mto_before

        res = super().write(values)

        templates_mto_after = self.filtered("is_mto")
        templates_not_mto_after = self - templates_mto_after

        templates_mto_added = templates_not_mto_before & templates_mto_after
        templates_mto_removed = templates_not_mto_after & templates_mto_before

        (
            templates_mto_added | templates_mto_removed
        ).product_variant_ids._compute_is_mto()

        return res

    @api.onchange("route_ids")
    def onchange_route_ids(self):
        mto_routes = self.env["stock.route"].search([("is_mto", "=", True)])
        if not mto_routes:
            return

        origin_routes = (
            self._origin.route_ids if self._origin else self.env["stock.route"]
        )
        current_routes = (
            self.route_ids._origin if self.route_ids else self.env["stock.route"]
        )

        added_routes = current_routes - origin_routes
        if set(mto_routes.ids) & set(added_routes.ids):
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

        removed_routes = origin_routes - current_routes
        if set(mto_routes.ids) & set(removed_routes.ids):
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
