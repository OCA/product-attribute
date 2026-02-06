from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    uom_factor_ids = fields.One2many(
        "product.uom.factor",
        "product_tmpl_id",
        string="UoM Conversion Factors",
    )

    def write(self, vals):
        res = super().write(vals)
        if "uom_ids" in vals:
            self._sync_uom_factor_ids()
        return res

    def _sync_uom_factor_ids(self):
        Factor = self.env["product.uom.factor"]
        for template in self:
            base_uom = template.uom_id
            cross_uoms = template.uom_ids.filtered(
                lambda u, bu=base_uom: not bu._has_common_reference(u)
            )
            existing = template.uom_factor_ids
            # Create missing factors for cross-category UoMs
            existing_uom_ids = existing.mapped("uom_id")
            for uom in cross_uoms - existing_uom_ids:
                Factor.create(
                    {
                        "product_tmpl_id": template.id,
                        "uom_id": uom.id,
                    }
                )
            # Delete factors whose UoM was removed from uom_ids
            to_delete = existing.filtered(lambda f, cu=cross_uoms: f.uom_id not in cu)
            to_delete.unlink()

    @api.constrains("uom_factor_ids")
    def _check_uom_factor_coverage(self):
        """Ensure variant coverage for each cross-category UoM.
        Auto-cleans duplicate catch-all lines and auto-creates missing
        catch-alls when not all variants are explicitly covered.
        Uses uom_ids (the template's allowed UoMs) as the source of truth
        for which UoMs need coverage, not just existing factor lines."""
        Factor = self.env["product.uom.factor"]
        for template in self:
            base_uom = template.uom_id
            cross_uoms = template.uom_ids.filtered(
                lambda u, bu=base_uom: not bu._has_common_reference(u)
            )
            for uom in cross_uoms:
                siblings = template.uom_factor_ids.filtered(
                    lambda f, u=uom: f.uom_id == u
                )
                # Auto-create catch-all if needed
                catchalls = siblings.filtered(lambda f: not f.product_ids)
                if not catchalls:
                    covered = siblings.mapped("product_ids")
                    if covered != template.product_variant_ids:
                        Factor.create(
                            {
                                "product_tmpl_id": template.id,
                                "uom_id": uom.id,
                            }
                        )
