# Copyright 2017-Today GRAP (http://www.grap.coop).
# Copyright 2018 ACSONE SA/NV
# Copyright 2018 Akretion (http://www.akretion.com).
# @author Sylvain LE GAL <https://twitter.com/legalsylvain>
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# @author Laurent Mignon <laurent.mignon@acsone.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    stock_state_threshold = fields.Float(
        compute="_compute_stock_state_threshold",
        store=True,
        help="Define custom value under which the stock state will pass from"
        " 'In Stock' to 'In Limited Stock' State. If not set, Odoo will"
        " use the value defined in the product category. If"
        " no value is defined in product category, it will use the value"
        " defined for the company",
        digits="Stock Threshold",
    )

    manual_stock_state_threshold = fields.Float(digits="Stock Threshold")

    @api.depends("categ_id.stock_state_threshold", "manual_stock_state_threshold")
    def _compute_stock_state_threshold(self):
        for rec in self:
            rec.stock_state_threshold = (
                rec.manual_stock_state_threshold or rec.categ_id.stock_state_threshold
            )
