# Copyright 2019 Akretion (http://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ExceptionRule(models.Model):
    _inherit = "exception.rule"

    model = fields.Selection(
        selection_add=[
            ("product.template", "Product Template"),
            ("product.product", "Product Variant"),
        ],
        ondelete={"product.template": "cascade", "product.product": "cascade"},
    )

    product_tmpl_ids = fields.Many2many("product.template", string="Product Templates")
