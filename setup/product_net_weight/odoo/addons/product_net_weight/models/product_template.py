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
        help="Net Weight of the product, container excluded.",
        store=True,
    )

    # Explicit field, renaming it
    weight = fields.Float(string="Gross Weight")

    @api.depends("product_variant_ids", "product_variant_ids.net_weight")
    def _compute_net_weight(self):
        unique_variants = self.filtered(lambda tmpl: tmpl.product_variant_count == 1)
        for template in unique_variants:
            template.net_weight = template.product_variant_ids.net_weight
        for template in self - unique_variants:
            template.net_weight = 0.0

    def _inverse_net_weight(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.net_weight = template.net_weight

    @api.model_create_multi
    def create(self, vals_list):
        templates = super(ProductTemplate, self).create(vals_list)
        # This is needed to set given values to first variant after creation
        for template, vals in zip(templates, vals_list):
            if vals.get("net_weight"):
                template.write({"net_weight": vals["net_weight"]})
        return templates
