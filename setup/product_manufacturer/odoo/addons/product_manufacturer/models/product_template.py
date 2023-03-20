# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    manufacturer = fields.Many2one(
        comodel_name="res.partner",
        compute="_compute_manufacturer_info",
        inverse="_inverse_manufacturer_info",
        store=True,
    )
    manufacturer_pname = fields.Char(
        compute="_compute_manufacturer_info",
        inverse="_inverse_manufacturer_info",
        store=True,
        string="Manuf. Product Name",
    )
    manufacturer_pref = fields.Char(
        compute="_compute_manufacturer_info",
        inverse="_inverse_manufacturer_info",
        store=True,
        string="Manuf. Product Code",
    )
    manufacturer_purl = fields.Char(
        compute="_compute_manufacturer_info",
        inverse="_inverse_manufacturer_info",
        store=True,
        string="Manuf. Product URL",
    )

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.manufacturer",
        "product_variant_ids.manufacturer_pname",
        "product_variant_ids.manufacturer_pref",
        "product_variant_ids.manufacturer_purl",
    )
    def _compute_manufacturer_info(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.manufacturer = template.product_variant_ids.manufacturer
            template.manufacturer_pname = (
                template.product_variant_ids.manufacturer_pname
            )
            template.manufacturer_pref = template.product_variant_ids.manufacturer_pref
            template.manufacturer_purl = template.product_variant_ids.manufacturer_purl
        for template in self - unique_variants:
            template.manufacturer = False
            template.manufacturer_pname = False
            template.manufacturer_pref = False
            template.manufacturer_purl = False

    def _inverse_manufacturer_info(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.manufacturer = template.manufacturer
                template.product_variant_ids.manufacturer_pname = (
                    template.manufacturer_pname
                )
                template.product_variant_ids.manufacturer_pref = (
                    template.manufacturer_pref
                )
                template.product_variant_ids.manufacturer_purl = (
                    template.manufacturer_purl
                )

    @api.model_create_multi
    def create(self, vals_list):
        """Overwrite creation for rewriting manufacturer information (if set and having
        only one variant), after the variant creation, that is performed in super.
        TODO : when migrating in version 16.0, remove the overload of the create function
        and overload instead the new function _get_related_fields_variant_template()
        introduced here : https://github.com/odoo/odoo/pull/82642
        """
        templates = super().create(vals_list)
        for template, vals in zip(templates, vals_list):
            if len(template.product_variant_ids) == 1:
                related_vals = {}
                if vals.get("manufacturer"):
                    related_vals["manufacturer"] = vals["manufacturer"]
                if vals.get("manufacturer_pname"):
                    related_vals["manufacturer_pname"] = vals["manufacturer_pname"]
                if vals.get("manufacturer_pref"):
                    related_vals["manufacturer_pref"] = vals["manufacturer_pref"]
                if vals.get("manufacturer_purl"):
                    related_vals["manufacturer_purl"] = vals["manufacturer_purl"]
                if related_vals:
                    template.write(related_vals)
        return templates
