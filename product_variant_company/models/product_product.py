# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Store related field
    company_id = fields.Many2one(
        related="product_tmpl_id.company_id", store=True, readonly=False, index=True
    )
