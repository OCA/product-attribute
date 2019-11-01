# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    dangerous_class = fields.Many2one(
        comodel_name="product.dangerous.class",
        ondelete="restrict",
        string="Dangerous Class",
    )
    is_dangerous_good = fields.Boolean(
        help="This product belongs to dangerous class"
    )
    is_dangerous_waste = fields.Boolean(
        help="Waste of this product belongs to dangerous class"
    )
    dangerous_component_ids = fields.One2many(
        "product.dangerous.component",
        "product_template_id",
        string="Dangerous components",
    )

    @api.constrains('dangerous_component_ids', 'dangerous_class')
    def _check_dangerous_choise(self):
        for record in self:
            if record.dangerous_component_ids and record.dangerous_class:
                raise ValidationError(
                    _(
                        "Product can contains danger products or be danger product by itself "
                    )
                )
