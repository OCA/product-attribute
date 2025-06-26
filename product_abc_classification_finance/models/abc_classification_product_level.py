from odoo import fields, models


class AbcClassificationProductLevel(models.Model):
    _inherit = "abc.classification.product.level"

    finance_sale_level_history_ids = fields.One2many(
        comodel_name="abc.finance.sale.level.history",
        inverse_name="product_level_id",
    )
