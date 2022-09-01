# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    picking_type_id = fields.Many2one(comodel_name="stock.picking.type")
