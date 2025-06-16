# Copyright 2025 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>

import json

from odoo import api, fields, models


class ProductPricelistItemAttributeValue(models.Model):
    _name = "product.pricelist.item.attribute.value"
    _description = "Product Pricelist Item Attribute Value"

    pricelist_item_id = fields.Many2one(
        comodel_name="product.pricelist.item",
        string="Pricelist Item",
    )
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        related="pricelist_item_id.product_tmpl_id",
    )

    available_attribute_value_domain = fields.Char(
        compute="_compute_available_attribute_domains",
    )

    additional_price = fields.Float(
        help="Additional price for the attribute value",
    )

    attribute_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        relation="pricelist_item_attribute_value_rel",
        string="Attribute Values",
    )

    @api.depends("product_tmpl_id")
    def _compute_available_attribute_domains(self):
        for rec in self:
            attr_lines = set(rec.product_tmpl_id.attribute_line_ids.value_ids.ids)
            used_values = set(
                rec.pricelist_item_id.pricelist_item_attribute_value_ids.attribute_value_ids.ids
            )
            available_values = list(attr_lines - used_values)
            domain = [("id", "in", available_values)]
            rec.available_attribute_value_domain = json.dumps(domain)
