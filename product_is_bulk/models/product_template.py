# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Quentin DUPONT (quentin.dupont@grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_bulk = fields.Boolean(
        compute=lambda x: x._compute_template_field_from_variant_field("is_bulk"),
        inverse=lambda x: x._set_product_variant_field("is_bulk"),
        readonly=False,
        help="Check this box if this product is sold without"
        " any manufactured packaging. It is usually the case"
        " for product whose unit of measure is a unit of weight"
        " or volume, but it can be also the case for products"
        " priced per unit but sold in bulk (such as cookies, bread, etc.)",
    )

    @api.onchange("uom_id")
    def _onchange_uom_id_is_bulk(self):
        self.is_bulk = self.uom_id.category_id.measure_type in [
            "weight",
            "volume",
        ]

    def _get_related_fields_variant_template(self):
        res = super()._get_related_fields_variant_template()
        res += ["is_bulk"]
        return res
