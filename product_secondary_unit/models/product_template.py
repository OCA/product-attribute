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
        """Helper to sync a template secondary UoM field from its variants.

        Can be used in modules depending on product_secondary_unit to implement
        compute methods for secondary UoM fields on product.template.

        The template field is a mirror of its variants: it shows the variants'
        value when they all share one, and is empty otherwise. This keeps the
        template field from displaying a value that no variant actually uses.

        :param str fname: name of the secondary UoM field to compute
        """
        for template in self:
            variant_values = template.product_variant_ids[fname]
            template[fname] = variant_values if len(variant_values) == 1 else False

    def _inverse_template_secondary_uom_field(self, fname):
        """Helper to propagate a template secondary UoM field to its variants.

        Can be used in modules depending on product_secondary_unit to implement
        inverse methods for secondary UoM fields on product.template.

        The template value is written to every variant, so that the template
        field keeps mirroring them. Use
        :meth:`_onchange_template_secondary_uom_field` to warn the user before
        overwriting variants that hold diverging values.

        :param str fname: name of the secondary UoM field to propagate
        """
        for template in self:
            template.product_variant_ids[fname] = template[fname]

    def _onchange_template_secondary_uom_field(self, fname):
        """Helper to warn that variants with distinct values will be overwritten.

        Can be used in modules depending on product_secondary_unit to implement
        onchange methods for secondary UoM fields on product.template.

        :param str fname: name of the secondary UoM field being set
        :return: an onchange warning, or None when variants do not diverge
        """
        self.ensure_one()
        variant_values = self.product_variant_ids[fname]
        if len(variant_values) <= 1:
            return None
        return {
            "warning": {
                "title": self.env._("Warning"),
                "message": self.env._(
                    "Product variants have distinct secondary units:"
                    "\n{secondary_uom}\n"
                    "All variants will be written with the new secondary unit."
                ).format(secondary_uom="\n".join(variant_values.mapped("name"))),
            }
        }

    @api.model_create_multi
    def create(self, vals_list):
        templates = super().create(vals_list)
        fnames = self._get_template_secondary_uom_fields()
        if not fnames:
            return templates
        # The inverse cannot reach the variant at create time, as it does not
        # exist yet, so the given values are written again once it does.
        for template, vals in zip(templates, vals_list, strict=True):
            related_vals = {fname: vals[fname] for fname in fnames if vals.get(fname)}
            if related_vals:
                template.write(related_vals)
        return templates

    def _get_template_secondary_uom_fields(self):
        """Return the names of the template secondary UoM mirror fields.

        These are the stored compute/inverse many2one fields to
        product.secondary.unit declared by modules depending on
        product_secondary_unit.
        """
        return [
            name
            for name, field in self._fields.items()
            if field.type == "many2one"
            and field.comodel_name == "product.secondary.unit"
            and field.store
            and field.compute
            and field.inverse
        ]
