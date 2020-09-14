# Copyright 2020 Camptocamp SA
# @author Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)

from odoo import models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "product.barcode.required.mixin"]

    def _create_variant_ids(self):
        return super(
            ProductTemplate, self.with_context(_bypass_barcode_required_check=True)
        )._create_variant_ids()
