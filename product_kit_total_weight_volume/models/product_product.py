#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    volume = fields.Float(
        compute="_compute_volume", store=True, readonly=False, recursive=True
    )
    weight = fields.Float(
        compute="_compute_weight", store=True, readonly=False, recursive=True
    )

    @api.depends("bom_ids", "bom_line_ids", "bom_line_ids.product_id.volume")
    def _compute_volume(self):
        for product in self.search([("is_kits", "=", True)]):
            bom_id = product.bom_ids.filtered(lambda bom: bom.type == "phantom")[:1]
            if bom_id:
                product_ids = bom_id[0].bom_line_ids.mapped("product_id")
                products = self.env["product.product"].browse(product_ids.ids)
                product.volume = sum(products.mapped("volume"))

    @api.depends("bom_ids", "bom_line_ids", "bom_line_ids.product_id.weight")
    def _compute_weight(self):
        for product in self.search([("is_kits", "=", True)]):
            bom_id = product.bom_ids.filtered(lambda bom: bom.type == "phantom")[:1]
            if bom_id:
                product_ids = bom_id[0].bom_line_ids.mapped("product_id")
                products = self.env["product.product"].browse(product_ids.ids)
                product.weight = sum(products.mapped("weight"))
