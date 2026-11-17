# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductPackagingTemplate(models.Model):
    _name = "product.packaging.template"
    _description = "Product Packaging Template"

    name = fields.Char("Product Packaging", required=True)
    sequence = fields.Integer(
        default=1, help="The first in the sequence is the default one."
    )
    product_tmpl_id = fields.Many2one(
        "product.template",
        string="Product Template",
        check_company=True,
        required=True,
        ondelete="cascade",
    )
    qty = fields.Float(
        "Contained Quantity",
        default=1,
        digits="Product Unit of Measure",
        help="Quantity of products contained in the packaging.",
    )
    company_id = fields.Many2one("res.company", "Company", index=True)
    packaging_ids = fields.One2many("product.packaging", "packaging_tmpl_id")

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for pt in res:
            pt.product_tmpl_id.product_variant_ids._create_packaging_from_template(
                template=pt
            )
        return res

    def write(self, vals):
        """
        Propagate changes on packages at variant level.
        """
        res = super().write(vals)
        self._propagate_to_packaging(vals)
        return res

    @api.model
    def _get_values_to_propagate(self, vals):
        return {key: vals[key] for key in {"name", "sequence", "qty"} if key in vals}

    def _propagate_to_packaging(self, vals):
        values_to_propagate = self._get_values_to_propagate(vals)
        if values_to_propagate:
            self.mapped("packaging_ids").write(values_to_propagate)

    def unlink(self):
        self.mapped("packaging_ids").unlink()
        return super().unlink()

    def _prepare_create_values_for_packaging(self):
        self.ensure_one()
        return {
            "name": self.name,
            "sequence": self.sequence,
            "qty": self.qty,
            "company_id": self.company_id.id,
            "packaging_tmpl_id": self.id,
        }
