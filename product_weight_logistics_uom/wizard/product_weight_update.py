# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductWeightUpdate(models.TransientModel):
    _inherit = "product.weight.update"

    def _get_component_weight(self, component, product_tmpl_id):
        """Weight according to product_tmpl_id's weight uom"""
        return component.weight_uom_id._compute_quantity(
            component.weight, product_tmpl_id.weight_uom_id
        )
