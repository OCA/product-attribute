# -*- coding: utf-8 -*-
# Copyright 2020 ForgeFlow
# Copyright 2021 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):

    _inherit = "product.product"

    abc_classification_product_level_ids = fields.One2many(
        "abc.classification.product.level", index=True, inverse_name="product_id"
    )
    abc_classification_profile_ids = fields.Many2many(
        comodel_name="abc.classification.profile",
        relation="abc_classification_profile_product_rel",
        column1="product_id",
        column2="profile_id",
        index=True,
    )
