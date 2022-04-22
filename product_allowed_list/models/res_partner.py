# Copyright 2021 - 2022 Camptocamp SA
# @author: Julien Coux <julien.coux@camptocamp.com>
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# @author: Damien Crier <damien.crier@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    product_allowed_list_ids = fields.Many2many("product.allowed.list")

    def _commercial_fields(self):
        return super()._commercial_fields() + ["product_allowed_list_ids"]
