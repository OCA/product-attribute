# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WizardModel(models.AbstractModel):
    _name = "alternative.product.wizard"
    _description = "Wizard that shows all the product alternatives"

    # order_line = fields.Many2one()
    product_id = fields.Many2one(comodel_name="product.product", readonly=True)
    name = fields.Char(related="product_id.name")
    qty = fields.Float(
        string="Quantity", digits="Product Unit of Measure", readonly=True
    )
    default_code = fields.Char(
        string="Internal Reference", related="product_id.default_code"
    )
    price_unit = fields.Float(digits="Product Price", readonly=True)
    operation_date = fields.Datetime()
    wizard_line_ids = fields.One2many(
        comodel_name="alternative.product.wizard.line",
        inverse_name="wizard_id",
        readonly=True,
    )

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        new_vals = self._get_order_line_field_vals()
        product_id = self.env["product.product"].browse(new_vals["product_id"])
        res.update(new_vals)
        res.update(self._get_wizard_line_vals(product_id))
        return res

    def _get_wizard_line_vals(self, product):
        return {
            "wizard_line_ids": [
                (0, 0, {"wizard_id": self.id, "alternative_product_id": alt.id})
                for alt in product.alternative_product_ids
            ]
        }

    @api.model
    def _get_order_line_field_vals(self):
        raise NotImplementedError


class AlternativeWizardLine(models.AbstractModel):
    _name = "alternative.product.wizard.line"
    _description = "Wizard that shows an alternative product"

    wizard_id = fields.Many2one(comodel_name="alternative.product.wizard")
    alternative_product_id = fields.Many2one(comodel_name="product.product")
    name = fields.Char(string="Name", related="alternative_product_id.name")
    default_code = fields.Char(
        string="Internal Reference", related="alternative_product_id.default_code"
    )
    price_unit = fields.Float(digits="Product Price", readonly=True)
