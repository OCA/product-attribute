# Copyright 2021 Camptocamp SA
# @author: Julien Coux <julien.coux@camptocamp.com>
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):

    _inherit = "res.company"

    default_seasonal_config_id = fields.Many2one(
        string="Default product seasonal configuration", comodel_name="seasonal.config"
    )

    def _create_default_seasonal_conf(self):
        self.ensure_one()
        if not self.default_seasonal_config_id:
            self.default_seasonal_config_id = self.env["seasonal.config"].create(
                {"name": _("Default product seasonal configuration: %s") % self.name}
            )

    @api.model
    def create(self, vals):
        company = super().create(vals)
        company._create_default_seasonal_conf()
        return company

    def write(self, vals):
        if "default_seasonal_config_id" in vals and not vals.get(
            "default_seasonal_config_id"
        ):
            raise ValidationError(
                _(
                    "Default product seasonal configuration is required: you can't remove it."
                )
            )
        return super().write(vals)
