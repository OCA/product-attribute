# Copyright (C) 2021 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    net_weight = fields.Float(
        compute="_compute_net_weight",
        inverse="_inverse_net_weight",
        digits="Stock Weight",
        help="Weight of the product without container nor packaging.",
        store=True,
    )

    # Explicit field, renaming it
    weight = fields.Float(
        string="Gross Weight",
        help="Weight of the product with its container and packaging.",
    )

    @api.depends("product_variant_ids.net_weight")
    def _compute_net_weight(self):
        self._compute_template_field_from_variant_field("net_weight")

    def _inverse_net_weight(self):
        self._set_product_variant_field("net_weight")

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        # This is needed to set given values to first variant after creation
        for template, vals in zip(templates, vals_list, strict=True):
            if vals.get("net_weight"):
                template.write({"net_weight": vals["net_weight"]})
        return templates
