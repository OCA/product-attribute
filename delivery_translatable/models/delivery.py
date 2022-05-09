# © 2022 Thomas Rehn (initOS GmbH)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    name = fields.Char(required=True, translate=True)
    website_description = fields.Text(
        string="Description for the website", translate=True
    )
