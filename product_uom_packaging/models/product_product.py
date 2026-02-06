from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Stored Many2many relationship (inverse of product_variant_ids)
    variant_packaging_ids = fields.Many2many(
        "product.uom.packaging",
        relation="product_uom_packaging_variant_rel",
        column1="product_id",
        column2="packaging_id",
        string="Variant-Specific Packaging",
        help="Packaging configurations specifically for this variant.",
    )

    # Computed field for template-level packaging (read-only)
    template_packaging_ids = fields.Many2many(
        "product.uom.packaging",
        compute="_compute_template_packaging_ids",
        string="Template Packaging",
        help="Packaging configurations inherited from product template.",
    )

    # Combined field (computed, read-only for display)
    packaging_ids = fields.Many2many(
        "product.uom.packaging",
        compute="_compute_packaging_ids",
        inverse="_inverse_packaging_ids",
        string="All Packaging",
        help="All packaging for this variant (template + variant).",
    )

    def action_open_template(self):
        """Open the product template form view."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "res_id": self.product_tmpl_id.id,
            "view_mode": "form",
            "target": "current",
        }

    @api.depends("product_tmpl_id.packaging_ids")
    def _compute_template_packaging_ids(self):
        """Compute template-level packaging configurations inherited by this variant."""
        for product in self:
            template_configs = self.env["product.uom.packaging"].search(
                [
                    ("product_tmpl_id", "=", product.product_tmpl_id.id),
                    ("company_id", "=", self.env.company.id),
                    ("product_variant_ids", "=", False),
                ]
            )
            product.template_packaging_ids = template_configs

    @api.depends("template_packaging_ids", "variant_packaging_ids")
    def _compute_packaging_ids(self):
        """Compute all packaging configurations for this variant."""
        for product in self:
            # Combine template-level and variant-level configs
            product.packaging_ids = (
                product.template_packaging_ids + product.variant_packaging_ids
            )

    def _inverse_packaging_ids(self):
        """
        Inverse function to handle changes to packaging configurations
        on the product template but not related to any specific variants.
        """
        for product in self:
            # Get current template packaging (excluding variant-specific ones)
            current_template_packaging = product.product_tmpl_id.packaging_ids.filtered(
                lambda p: not p.product_variant_ids
            )

            # Get desired packaging from computed field (excl. variant-specific)
            variant_packaging = product.variant_packaging_ids
            desired_packaging = product.packaging_ids.filtered(
                lambda p, vp=variant_packaging: p not in vp
            )

            # Find packaging to remove (in current but not in desired)
            to_remove = current_template_packaging - desired_packaging
            # Find packaging to add (in desired but not in current)
            to_add = desired_packaging - current_template_packaging

            # Remove unwanted packaging
            if to_remove:
                to_remove.unlink()

            # Add new packaging by setting the correct template. Only clear
            # product_variant_ids if it was already empty (template-level)
            if to_add:
                for packaging in to_add:
                    if not packaging.product_variant_ids:
                        packaging.write(
                            {
                                "product_tmpl_id": product.product_tmpl_id.id,
                                "product_variant_ids": False,
                            }
                        )
                    else:
                        # This is variant-specific packaging, just set the template
                        packaging.write(
                            {
                                "product_tmpl_id": product.product_tmpl_id.id,
                            }
                        )
