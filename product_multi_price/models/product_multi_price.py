# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductMultiPrice(models.Model):
    _name = "product.multi.price"
    _rec_name = "name_text"
    _description = "Product Multiple Prices"

    name = fields.Many2one(
        "product.multi.price.name",
        required=True,
        ondelete="cascade",
    )
    name_text = fields.Char(related="name.name")
    product_id = fields.Many2one(
        comodel_name="product.product",
        required=True,
        ondelete="cascade",
    )
    price = fields.Float(
        digits="Product Price",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        related="name.company_id",
        store=True,
        readonly=True,
    )

    @api.constrains("name", "product_id", "company_id")
    def _check_name_product_id_company_id(self):
        for rec in self:
            domain = [
                ("id", "!=", rec.id),
                ("name", "=", rec.name.id),
                ("product_id", "=", rec.product_id.id),
            ]
            if rec.company_id:
                domain.append(("company_id", "=", rec.company_id.id))
            else:
                domain.append(("company_id", "=", False))
            if self.with_context(active_test=False).search_count(domain):
                raise ValidationError(
                    self.env._(
                        "A field name can not be assigned twice to a "
                        "product for the same company"
                    )
                )


class ProductMultiPriceName(models.Model):
    _name = "product.multi.price.name"
    _description = "Multi Price Record Options"

    @api.model
    def _get_company(self):
        # Get company from context if explicitly provided, otherwise allow None to
        # represent a global/shared field that isn't tied to any specific company
        return self.env.context.get("company_id", False)

    name = fields.Char(required=True, string="Price Field Name")
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=False,
        default=lambda self: self._get_company(),
    )

    @api.constrains("name", "company_id")
    def _check_name_company_id(self):
        for rec in self:
            if not rec.company_id:
                continue
            domain = [
                ("id", "!=", rec.id),
                ("name", "=", rec.name),
                ("company_id", "=", rec.company_id.id),
            ]
            if self.with_context(active_test=False).search_count(domain):
                raise ValidationError(
                    self.env._("Prices Names must be unique per company")
                )
