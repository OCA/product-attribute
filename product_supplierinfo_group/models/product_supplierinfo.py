# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import api, fields, models
from copy import deepcopy

# format: field_from_supplierinfo:field_from_group
MAPPING_RELATED = {
    "product_tmpl_id": "product_tmpl_id",
    "name": "partner_id",
    "product_id": "product_id",
    "product_name": "product_name",
    "product_code": "product_code",
    "sequence": "sequence",
}

MAPPING_MATCH_GROUP = {
    "product_tmpl_id": "product_tmpl_id",
    "name": "partner_id",
    "product_id": "product_id",
    "product_name": "product_name",
    "product_code": "product_code",
}
_logger = logging.getLogger(__name__)


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    supplierinfo_group_id = fields.Many2one("product.supplierinfo.group", required=True)
    product_tmpl_id = fields.Many2one(
        related="supplierinfo_group_id.product_tmpl_id", store=True
    )
    name = fields.Many2one(related="supplierinfo_group_id.partner_id", store=True)
    product_id = fields.Many2one(related="supplierinfo_group_id.product_id", store=True)
    product_name = fields.Char(related="supplierinfo_group_id.product_name", store=True)
    product_code = fields.Char(related="supplierinfo_group_id.product_code", store=True)
    sequence = fields.Integer(related="supplierinfo_group_id.sequence", store=True)

    def _find_or_create_supplierinfo_group(self, vals):
        domain = [
            (field_group, "=", vals.get(field_supplierinfo))
            for field_supplierinfo, field_group in MAPPING_MATCH_GROUP.items()
        ]
        group = self.env["product.supplierinfo.group"].search(domain)
        if not group:
            group = self.env["product.supplierinfo.group"].create(
                {
                    field_group: vals.get(field_supplierinfo)
                    for field_supplierinfo, field_group in MAPPING_MATCH_GROUP.items()
                }
            )
        return group

    def to_supplierinfo_group(self, vals):
        new_val = deepcopy(vals)
        group = self.env["product.supplierinfo.group"].browse(
            new_val.get("supplierinfo_group_id")
        ) or self._find_or_create_supplierinfo_group(new_val)
        new_val["supplierinfo_group_id"] = group.id
        for field_supplierinfo in MAPPING_RELATED.keys():
            if field_supplierinfo in new_val:
                del new_val[field_supplierinfo]
        return new_val

    @api.model_create_multi
    def create(self, vals):
        new_vals = []
        for el in vals:
            new_vals.append(self.to_supplierinfo_group(el))
        return super().create(new_vals)
