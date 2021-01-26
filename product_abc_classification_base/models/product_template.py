# -*- coding: utf-8 -*-
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    abc_product_classification_level_ids = fields.Many2many(
        related="product_variant_ids.abc_product_classification_level_ids"
    )
    abc_classification_profile_ids = fields.Many2many(
        related="product_variant_ids.abc_classification_profile_ids"
    )
