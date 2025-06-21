from odoo import fields, models

class AbcFinanceSaleLevelHistory(models.Model):
    """Finance ABC Classification Product Level History"""
    _name = "abc.finance.sale.level.history"
    _description = "Abc Finance Sale Level History"

    computed_level_id = fields.Many2one(
        "abc.classification.level",
        string="Computed classification level",
        readonly=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        index=True,
        required=True,
        readonly=True,
        ondelete="cascade",
    )
    product_tmpl_id = fields.Many2one(
        "product.template",
        string="Product template",
        related="product_id.product_tmpl_id",
        readonly=True,
        store=True,
    )
    purchase_price = fields.Float(
        "Purchase price",
        required=True,
        readonly=True,
    )
    margin = fields.Float(
        "Margin",
        required=True,
        readonly=True,
    )
    total_cost = fields.Float(
        "Total cost",
        required=True,
        readonly=True,
    )
    total_sales = fields.Float(
        "Total sales",
        required=True,
        readonly=True,
    )
    profile_id = fields.Many2one(
        "abc.classification.profile",
        string="Profile",
        required=True,
        readonly=True,
        ondelete="cascade",
    )
    warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Warehouse",
        readonly=True,
        ondelete="cascade",
    )
    ranking = fields.Integer("Ranking", readonly=True)
    percentage = fields.Float("Percentage", readonly=True)
    cumulated_percentage = fields.Float("Cumulated Percentage", readonly=True)
    standard_cost = fields.Float("Standard Cost", readonly=True)
    total_cost = fields.Float("Total Cost", readonly=True)
    total_sales = fields.Float("Total Sales", readonly=True)
    margin = fields.Float("Margin", readonly=True)
    product_level_id = fields.Many2one(
        "abc.classification.product.level",
        string="Product Level",
        readonly=True,
        ondelete="cascade",
    )
    from_date = fields.Date(readonly=True)
    to_date = fields.Date(readonly=True)
    total_products = fields.Integer(readonly=True)
    percentage_products = fields.Float(readonly=True)
    cumulated_percentage_products = fields.Float(readonly=True)
    sum_cumulated_percentages = fields.Float(readonly=True)
