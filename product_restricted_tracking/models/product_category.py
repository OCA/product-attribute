# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _inherit = "product.category"

    restricted_tracking = fields.Selection(
        selection=lambda self: self.env["product.template"]
        ._fields["tracking"]
        ._description_selection(self.env),
    )

    @api.constrains("restricted_tracking")
    def _check_restricted_tracking(self):
        for categ in self:
            if not categ.restricted_tracking:
                continue
            conflicting_products = self.env["product.template"].search(
                [
                    ("categ_id", "=", categ.id),
                    ("tracking", "!=", categ.restricted_tracking),
                ]
            )
            if conflicting_products:
                tracking_label = dict(
                    categ._fields["restricted_tracking"]._description_selection(
                        self.env
                    )
                ).get(categ.restricted_tracking)
                tracking_selection_dict = dict(
                    conflicting_products._fields["tracking"]._description_selection(
                        self.env
                    )
                )
                total_count = len(conflicting_products)
                product_list = "\n".join(
                    [
                        "- %s (%s)"
                        % (
                            product.display_name,
                            tracking_selection_dict.get(product.tracking),
                        )
                        for product in conflicting_products[:10]
                    ]
                )
                more_info = (
                    _("\n... and %s more product(s)", total_count - 10)
                    if total_count > 10
                    else ""
                )
                raise ValidationError(
                    _(
                        "Cannot set restricted tracking to '%(tracking)s' because "
                        "%(count)s product(s) in this category have different "
                        "tracking:\n%(products)s%(more)s",
                        tracking=tracking_label,
                        count=total_count,
                        products=product_list,
                        more=more_info,
                    )
                )
