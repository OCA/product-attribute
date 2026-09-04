from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    reservation_lead_days = fields.Integer(
        string="Default Reservation Lead Time (days)",
        default=15,
        help="Global reservation lead time used when a product's category "
        "(or its ancestors) has no specific rule",
    )
