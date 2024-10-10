# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    manufacturer_id = fields.Many2one(
        comodel_name="res.partner",
        compute="_compute_manufacturer_info",
        inverse="_inverse_manufacturer_info",
        store=True,
    )
    manufacturer_pname = fields.Char(
        compute="_compute_manufacturer_info",
        inverse="_inverse_manufacturer_info",
        store=True,
        string="Manufacturer Product Name",
    )
    manufacturer_pref = fields.Char(
        compute="_compute_manufacturer_info",
        inverse="_inverse_manufacturer_info",
        store=True,
        string="Manufacturer Product Code",
    )
    manufacturer_purl = fields.Char(
        compute="_compute_manufacturer_info",
        inverse="_inverse_manufacturer_info",
        store=True,
        string="Manufacturer Product URL",
    )

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.manufacturer_id",
        "product_variant_ids.manufacturer_pname",
        "product_variant_ids.manufacturer_pref",
        "product_variant_ids.manufacturer_purl",
    )
    def _compute_manufacturer_info(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            product_variant = template.product_variant_ids
            template.update(
                {
                    "manufacturer_id": product_variant.manufacturer_id.id,
                    "manufacturer_pname": product_variant.manufacturer_pname,
                    "manufacturer_pref": product_variant.manufacturer_pref,
                    "manufacturer_purl": product_variant.manufacturer_purl,
                }
            )
        (self - unique_variants).update(
            {
                "manufacturer_id": False,
                "manufacturer_pname": False,
                "manufacturer_pref": False,
                "manufacturer_purl": False,
            }
        )

    def _inverse_manufacturer_info(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.update(
                    {
                        "manufacturer_id": template.manufacturer_id,
                        "manufacturer_pname": template.manufacturer_pname,
                        "manufacturer_pref": template.manufacturer_pref,
                        "manufacturer_purl": template.manufacturer_purl,
                    }
                )

    def _get_related_fields_variant_template(self):
        """Adds fields related to manufacturer that are present on template and
        variants models"""
        res = super()._get_related_fields_variant_template()
        res.extend(
            [
                "manufacturer_id",
                "manufacturer_pname",
                "manufacturer_pref",
                "manufacturer_purl",
            ]
        )
        return res
