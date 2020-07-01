# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    @api.onchange("packaging_type_id")
    def _onchange_name(self):
        if self.packaging_type_id:
            self.name = self.packaging_type_id.name

    def name_get(self):
        result = []
        for record in self:
            if record.product_id and record.packaging_type_id:
                result.append((record.id, record.packaging_type_id.display_name))
            else:
                result.append((record.id, record.name))
        return result
