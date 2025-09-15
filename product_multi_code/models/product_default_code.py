# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductDefaultCode(models.Model):
    _name = "product.default_code"
    _description = "Internal reference entry for a product"
    _order = "sequence, id"

    name = fields.Char(
        string="Internal Reference",
        required=True,
    )
    sequence = fields.Integer(default=10)

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        compute="_compute_product",
        store=True,
        readonly=False,
        ondelete="cascade",
    )
    product_tmpl_id = fields.Many2one(
        "product.template",
        compute="_compute_product_tmpl",
        store=True,
        readonly=False,
        ondelete="cascade",
    )

    @api.depends("product_id")
    def _compute_product_tmpl(self):
        for rec in self.filtered(lambda x: not x.product_tmpl_id and x.product_id):
            rec.product_tmpl_id = rec.product_id.product_tmpl_id

    @api.depends("product_tmpl_id.product_variant_ids")
    def _compute_product(self):
        for rec in self.filtered(
            lambda x: not x.product_id and x.product_tmpl_id.product_variant_ids
        ):
            rec.product_id = rec.product_tmpl_id.product_variant_ids[0]

    def _get_domain_check_duplicates(self):
        return [("id", "not in", self.ids), ("name", "in", self.mapped("name"))]

    @api.constrains("name")
    def _check_duplicates(self):
        codes_to_check = self.sudo().search(self._get_domain_check_duplicates())
        for record in self:
            duplicate = codes_to_check.filtered(
                lambda b, rec=record: b.name == rec.name
            )

            if duplicate:
                product = duplicate[0].sudo().product_id
                raise ValidationError(
                    f'The Internal Reference "{record.name}" already exists for '
                    f'product "{product.name}".'
                )

    @api.constrains("product_id", "product_tmpl_id")
    def _check_required_product(self):
        for rec in self:
            if not (rec.product_id or rec.product_tmpl_id):
                raise ValidationError(
                    f'You must assign the internal reference "{rec.name}" '
                    "to a product or a template."
                )
