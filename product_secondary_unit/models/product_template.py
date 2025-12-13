# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    secondary_uom_ids = fields.One2many(
        comodel_name="product.secondary.unit",
        inverse_name="product_tmpl_id",
        string="Secondary Unit of Measure",
        help="Default Secondary Unit of Measure.",
        context={"active_test": False},
    )

    @api.model
    def _get_default_secondary_uom(self):
        return (
            self.secondary_uom_ids
            and self.secondary_uom_ids[0]
            or self.secondary_uom_ids
        )

    def _compute_template_secondary_uom_field(self, fname):
        """Helper to sync template secondary UoM field from variant.

        Can be used in modules depending on product_secondary_unit to implement
        compute methods for secondary UoM fields on product.template.

        - Single variant: Sync the variant's value to the template
        - Multiple variants: Keep the existing template value

        :param str fname: name of the secondary UoM field to compute
        """
        for template in self:
            if len(template.product_variant_ids) == 1:
                template[fname] = template.product_variant_ids[fname]
            # Keep existing value when multiple variants (don't clear)

    def _inverse_template_secondary_uom_field(self, fname):
        """Helper to propagate template secondary UoM field to variants.

        Can be used in modules depending on product_secondary_unit to implement
        inverse methods for secondary UoM fields on product.template.

        - Single variant: Always sync the template's value to the variant
        - Multiple variants: Only update variants without their own setting

        :param str fname: name of the secondary UoM field to propagate
        """
        for template in self:
            if len(template.product_variant_ids) == 1:
                variants_to_update = template.product_variant_ids
            else:
                variants_to_update = template.product_variant_ids.filtered(
                    lambda v, f=fname: not v[f]
                )
            variants_to_update[fname] = template[fname]
