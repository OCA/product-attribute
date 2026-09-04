from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    reservation_lead_days = fields.Integer(
        related="company_id.reservation_lead_days",
        readonly=False,
        string="Default Reservation Lead Time (days)",
    )
