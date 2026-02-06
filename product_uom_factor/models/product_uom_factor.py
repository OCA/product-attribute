from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductUomFactor(models.Model):
    _name = "product.uom.factor"
    _description = "Product-specific UoM Conversion Factor"

    product_tmpl_id = fields.Many2one(
        "product.template",
        string="Product Template",
        required=True,
        readonly=True,
        index=True,
        ondelete="cascade",
    )
    product_ids = fields.Many2many(
        "product.product",
        string="Variants",
        help="Specific variants this factor applies to. "
        "Leave empty to apply to all variants.",
    )
    uom_id = fields.Many2one(
        "uom.uom",
        "Unit of Measure",
        required=True,
        readonly=True,
        index=True,
        ondelete="cascade",
    )
    factor = fields.Float(
        "Conversion Factor",
        default=1.0,
        required=True,
        help="Product-specific conversion factor for cross-category UoM "
        "conversions. Represents how many of the product's base UoM equal "
        "one unit of this UoM. For example, for ink with a specific "
        "gravity of 1.05 and base UoM of grams, the factor on the mL "
        "UoM would be 1.05 (1 mL = 1.05 g).",
    )

    def write(self, vals):
        res = super().write(vals)
        if "product_ids" in vals:
            self.mapped("product_tmpl_id")._check_uom_factor_coverage()
        return res

    def unlink(self):
        templates = self.mapped("product_tmpl_id")
        res = super().unlink()
        templates._check_uom_factor_coverage()
        return res

    @api.constrains("product_ids", "product_tmpl_id")
    def _check_product_ids_same_template(self):
        for rec in self:
            if rec.product_ids and any(
                p.product_tmpl_id != rec.product_tmpl_id for p in rec.product_ids
            ):
                raise ValidationError(
                    self.env._("All variants must belong to the same product template.")
                )

    @api.constrains("product_ids", "uom_id", "product_tmpl_id")
    def _check_no_duplicate_factors(self):
        """Auto-clean duplicate factor lines, then raise if any remain.
        A duplicate is defined as two records with the same
        (uom_id, product_tmpl_id, frozenset(product_ids))."""
        tmpl_uom_pairs = {(rec.product_tmpl_id.id, rec.uom_id.id) for rec in self}
        for tmpl_id, uom_id in tmpl_uom_pairs:
            siblings = self.search(
                [
                    ("product_tmpl_id", "=", tmpl_id),
                    ("uom_id", "=", uom_id),
                ]
            )
            keys = []
            to_delete = self.browse()
            for sib in siblings:
                key = (uom_id, tmpl_id, frozenset(sib.product_ids.ids))
                if key in keys:
                    to_delete |= sib
                else:
                    keys.append(key)
            if to_delete:
                to_delete.unlink()

    @api.constrains("factor", "uom_id", "product_tmpl_id")
    def _check_same_category_factor(self):
        for rec in self:
            base_uom = rec.product_tmpl_id.uom_id
            if base_uom._has_common_reference(rec.uom_id):
                expected = rec.uom_id.factor / base_uom.factor
                if rec.factor != expected:
                    raise ValidationError(
                        self.env._(
                            "The conversion factor for %(uom)s cannot be "
                            "customized because it is in the same category "
                            "as the product's base UoM (%(base_uom)s). "
                            "Expected factor: %(expected)s.",
                            uom=rec.uom_id.name,
                            base_uom=base_uom.name,
                            expected=expected,
                        )
                    )
