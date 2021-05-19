# Copyright 2021 Camptocamp SA
# @author: Julien Coux <julien.coux@camptocamp.com>
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    seasonal_config_id = fields.Many2one(
        string="Product seasonal configuration", comodel_name="seasonal.config"
    )

    def _commercial_fields(self):
        return super()._commercial_fields() + ["seasonal_config_id"]
