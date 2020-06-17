# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductPricelistItem(models.Model):

    _inherit = "product.pricelist.item"

    assortment_item_id = fields.Many2one(
        comodel_name="product.pricelist.assortment.item",
        string="Assortment item",
        readonly=True,
        ondelete="cascade",
    )
