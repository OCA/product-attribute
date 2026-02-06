from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductUomPackaging(models.Model):
    _name = "product.uom.packaging"
    _description = "Product UoM Packaging Configuration"
    _order = "sequence, id"

    name = fields.Char(
        help="Display name for the packaging configuration.",
        required=True,
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
    qty = fields.Float(
        "Qty per Package",
        default=1.0,
        required=True,
        help="How many of the selected UoM fit inside one package. "
        "For example, if the UoM is 'Pack of 6' and qty is 2, "
        "the package contains 2 packs of 6 (12 units total).",
    )
    package_type_id = fields.Many2one(
        "stock.package.type",
        "Package Type",
        required=True,
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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") and vals.get("package_type_id"):
                package_type = self.env["stock.package.type"].browse(
                    vals["package_type_id"]
                )
                vals["name"] = package_type.name
        return super().create(vals_list)

    @api.onchange("package_type_id")
    def _onchange_package_type_id(self):
        """Default name to package type name when package type is set."""
        for record in self:
            if record.package_type_id and not record.name:
                record.name = record.package_type_id.name

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

    @api.constrains(
        "product_tmpl_id",
        "product_variant_ids",
        "company_id",
        "uom_id",
        "package_type_id",
        "qty",
    )
    def _check_unique_packaging(self):
        """Ensure only one packaging per template/UoM/qty/package_type/company."""
        for record in self:
            template = record.product_tmpl_id
            unicity_keys = [
                (
                    r.product_tmpl_id.id,
                    r.uom_id.id,
                    r.company_id.id,
                    tuple(r.product_variant_ids.ids),
                    r.package_type_id.id,
                    r.qty,
                )
                for r in template.packaging_ids
            ]
            if len(unicity_keys) != len(set(unicity_keys)):
                raise ValidationError(
                    self.env._(
                        "Duplicate packaging configuration found for the same "
                        "product template, UoM, quantity, company, "
                        "and package type."
                    )
                )

    @api.constrains("name", "product_tmpl_id", "company_id")
    def _check_unique_name(self):
        """Ensure packaging name is unique per product template and company."""
        for record in self:
            template = record.product_tmpl_id
            name_keys = [
                (r.name, r.product_tmpl_id.id, r.company_id.id)
                for r in template.packaging_ids
                if r.name
            ]
            if len(name_keys) != len(set(name_keys)):
                raise ValidationError(
                    self.env._(
                        "Packaging name must be unique per product template "
                        "and company."
                    )
                )
