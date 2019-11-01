# Copyright 2019 Iryna Vyshnevska (Camptocamp)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, models, fields


class ProductDangerousComponent(models.Model):
    _name = "product.dangerous.component"
    _description = "Product Dangerous Component"

    product_template_id = fields.Many2one(
        comodel_name="product.template", required=True, ondelete="cascade"
    )
    component_product_id = fields.Many2one(
        comodel_name="product.template", string="Product", required=True
    )
    dangerous_class = fields.Many2one(
        comodel_name="product.dangerous.class",
        related="component_product_id.dangerous_class",
        ondelete="restrict",
        string="Dangerous Class",
    )
    weight = fields.Float(
        help="The weight of dangerous product in main product."
    )
    volume = fields.Float(
        help="The volume of dangerous product in main product."
    )
    weight_uom_id = fields.Many2one(
        comodel_name="uom.uom", string="Weight UoM"
    )
    volume_uom_id = fields.Many2one(
        comodel_name="uom.uom", string="Volume UoM"
    )
