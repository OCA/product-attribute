# -*- coding: utf-8 -*-
# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import fields, models


class ProductPackagingType(models.Model):
    _inherit = "product.packaging.type"

    is_pallet = fields.Boolean()
