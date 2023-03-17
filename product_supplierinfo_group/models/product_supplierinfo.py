# Copyright 2020 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models

# format: field_from_supplierinfo:field_from_group
MAPPING_MATCH_GROUP = {
    "company_id": "company_id",
    "product_tmpl_id": "product_tmpl_id",
    "name": "partner_id",
    "product_id": "product_id",
    "product_name": "product_name",
    "product_code": "product_code",
}

_logger = logging.getLogger(__name__)


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    group_id = fields.Many2one(
        "product.supplierinfo.group",
        required=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(related="group_id.company_id", store=True)
    product_tmpl_id = fields.Many2one(related="group_id.product_tmpl_id", store=True)
    name = fields.Many2one(related="group_id.partner_id", store=True, required=False)
    product_id = fields.Many2one(related="group_id.product_id", store=True)
    product_name = fields.Char(related="group_id.product_name", store=True)
    product_code = fields.Char(related="group_id.product_code", store=True)
    sequence = fields.Integer(related="group_id.sequence", store=True)

    _sql_constraints = [
        (
            "uniq_price_per_qty",
            "unique(group_id, min_qty, date_start, date_end)",
            "You can not have a two price for the same qty",
        )
    ]

    def _fields_for_group_match(self):
        return MAPPING_MATCH_GROUP

    def _none_writable_related_fields(self):
        return list(self._fields_for_group_match().keys()) + ["sequence"]

    def _get_existing_group(self, field_mapping, vals):
        return self.env["product.supplierinfo.group"].search(
            [
                (field_group, "=", vals.get(field_supplierinfo))
                for field_supplierinfo, field_group in field_mapping
            ]
        )

    def _get_or_create_group(self, vals):
        field_mapping = self._fields_for_group_match().items()
        group = self._get_existing_group(field_mapping, vals)
        if not group:
            group = self.env["product.supplierinfo.group"].create(
                {
                    field_group: vals.get(field_supplierinfo)
                    for field_supplierinfo, field_group in field_mapping
                }
            )
        return group

    @api.model_create_multi
    def create(self, list_vals):
        if not self.env.context.get("skip_group_specific"):
            for vals in list_vals:
                if not vals.get("group_id"):
                    vals["group_id"] = self._get_or_create_group(vals).id
                    # remove useless related fields
                    for field_name in self._none_writable_related_fields():
                        vals.pop(field_name, None)
        return super().create(list_vals)
