# © 2020 Akretion France
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _create_variant_ids(self):
        if not self._context.get("skip_create_variant"):
            return super()._create_variant_ids()

    def update_attribute(self, values):
        self.ensure_one()
        self = self.with_context(skip_create_variant=True)
        for value in values:
            match = False
            for line in self.attribute_line_ids:
                if line.attribute_id == value.attribute_id:
                    line.value_ids |= value
                    match = True
            if not match:
                self.env["product.template.attribute.line"].create({
                    "product_tmpl_id": self.id,
                    "attribute_id": value.attribute_id.id,
                    "value_ids": [(6, 0, [value.id])],
                    })
        active_variants = self.product_variant_ids
        self.with_context(skip_create_variant=False)._create_variant_ids()
        self.flush()
        variant = self._get_existing_variant(values)
        # Inactive all unwanted variant
        (self.product_variant_ids - active_variants - variant).write({"active": False})

    def _get_existing_variant(self, values):
        self.ensure_one()
        for record in self.with_context(active_test=False).product_variant_ids:
            if record.attribute_value_ids == values:
                return record
        else:
            raise UserError(
                "No matching variant found, maybe the attribute value are incoherant ")
