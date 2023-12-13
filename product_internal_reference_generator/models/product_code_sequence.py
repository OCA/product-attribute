# Copyright 2023 Ooops - Ilyas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, exceptions, fields, models


class ProductCodeSequence(models.Model):
    _name = "product.code.sequence"
    _description = "Internal Reference Template"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    sequence_id = fields.Many2one("ir.sequence", required=True)
    variant_reference_numbers = fields.Integer("Digits", default=3, required=True)

    def unlink(self):
        for rec in self:
            products = self.env["product.template"].search(
                [("int_ref_template_id", "=", rec.id)]
            )
            if products:
                raise exceptions.ValidationError(
                    _(
                        "You can't delete %s template because there are products "
                        "related to it. You can archive it instead.\n"
                        "Products: '%s'"
                        % (rec.name, ", ".join(products.mapped("display_name")))
                    )
                )
        return super().unlink()
