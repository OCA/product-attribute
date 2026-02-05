# Copyright 2025 Rod Wilson Industries
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductUomPackaging(models.Model):
    _name = "product.uom.packaging"
    _description = "Product UoM Packaging Configuration"
    _order = "sequence, id"

    name = fields.Char(
        compute="_compute_name",
        store=True,
        help="Display name for the packaging configuration.",
    )
    sequence = fields.Integer(
        default=10,
        help="Order in which packaging configurations are displayed.",
    )

    # Core fields - template is required, variants are optional
    product_tmpl_id = fields.Many2one(
        "product.template",
        "Product Template",
        required=True,
        index=True,
        help="Product template this packaging configuration belongs to.",
    )
    product_variant_ids = fields.Many2many(
        comodel_name="product.product",
        relation="product_uom_packaging_variant_rel",
        column1="packaging_id",
        column2="product_id",
        string="Product Variants",
        help="Limit to specific variants. If empty, applies to all variants.",
    )

    # Packaging details
    uom_id = fields.Many2one(
        "uom.uom",
        "Unit of Measure",
        required=True,
        ondelete="restrict",
        index=True,
        help="Unit of measure for this packaging configuration.",
    )
    package_type_id = fields.Many2one(
        "stock.package.type",
        "Package Type",
        ondelete="restrict",
        help="Package type defines the physical dimensions of the packaging.",
    )
    company_id = fields.Many2one(
        "res.company",
        "Company",
        default=lambda self: self.env.company,
        index=True,
        help="Company this packaging configuration belongs to.",
    )

    @api.depends("product_tmpl_id.name", "uom_id.name", "package_type_id.name")
    def _compute_name(self):
        """Generate display name for the packaging configuration."""
        for record in self:
            parts = []
            if record.product_tmpl_id:
                parts.append(record.product_tmpl_id.name)
            if record.uom_id:
                parts.append(record.uom_id.name)
            if record.package_type_id:
                parts.append(record.package_type_id.name)

            record.name = f"{' - '.join(parts)}"

    @api.constrains("product_tmpl_id", "product_variant_ids")
    def _check_product_variant_ids(self):
        """Ensure product_variant_ids belongs to the product_tmpl_id."""
        for record in self:
            if record.product_variant_ids:
                if any(
                    variant.product_tmpl_id != record.product_tmpl_id
                    for variant in record.product_variant_ids
                ):
                    raise ValidationError(
                        self.env._(
                            "All product variants must belong to the same "
                            "product template."
                        )
                    )

    @api.constrains("product_tmpl_id", "product_variant_ids", "company_id", "uom_id")
    def _check_unique_packaging(self):
        """Ensure only one packaging per template/UoM/company combination."""
        for record in self.filtered("product_variant_ids"):
            rec_id = record.id
            rec_uom = record.uom_id
            rec_company = record.company_id
            for variant in record.product_variant_ids:
                other_packaging = variant.variant_packaging_ids.filtered(
                    lambda p, rid=rec_id, uom=rec_uom, comp=rec_company: (
                        p.id != rid and p.uom_id == uom and p.company_id == comp
                    )
                )
                if other_packaging:
                    raise ValidationError(
                        self.env._(
                            "There is already a packaging configuration for "
                            "this template/UoM/company combination."
                        )
                    )
        for record in self.filtered(
            lambda r: r.product_tmpl_id and not r.product_variant_ids
        ):
            rec_id = record.id
            rec_uom = record.uom_id
            rec_company = record.company_id
            other_packaging = record.product_tmpl_id.packaging_ids.filtered(
                lambda p, rid=rec_id, uom=rec_uom, comp=rec_company: (
                    p.id != rid
                    and p.uom_id == uom
                    and p.company_id == comp
                    and not p.product_variant_ids
                )
            )
            if other_packaging:
                raise ValidationError(
                    self.env._(
                        "There is already a packaging configuration for "
                        "this template/UoM/company combination."
                    )
                )
