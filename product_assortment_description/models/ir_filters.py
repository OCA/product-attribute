from odoo import fields, models


class IrFilters(models.Model):
    _name = "ir.filters"
    _inherit = ["ir.filters", "mail.thread", "mail.activity.mixin"]

    description = fields.Text("Description")
