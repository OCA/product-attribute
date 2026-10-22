# Copyright 2021 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)

from odoo import models


class Product(models.Model):
    _inherit = "product.product"

    def _packaging_name_getter(self, packaging):
        if packaging and packaging._name == "product.uom":
            packaging_level = packaging.uom_id.packaging_level_id
        else:
            packaging_level = packaging.packaging_level_id if packaging else False

        if packaging_level:
            return packaging_level.name
        if not packaging:
            return False
        return super()._packaging_name_getter(packaging)

    def _qty_by_packaging_as_str(self, packaging, qty):
        # By default use packaging type code
        qty_by_packaging_level_fname = self.env.context.get(
            "qty_by_packaging_level_fname", "code"
        )
        compact_mode = self.env.context.get("qty_by_packaging_level_compact", True)
        sep = "" if compact_mode else " "
        # Override to use packaging level code
        if packaging and packaging._name == "product.uom":
            packaging_level = packaging.uom_id.packaging_level_id
        else:
            packaging_level = packaging.packaging_level_id if packaging else False

        if packaging_level:
            name = packaging_level[qty_by_packaging_level_fname] or ""
            return f"{qty}{sep}{name}"
        if not packaging:
            return False
        return super()._qty_by_packaging_as_str(packaging, qty)
