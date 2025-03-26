# Copyright (C) 2025  Renato Lima - Akretion
# License LGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from odoo.osv import expression


class Uom(models.Model):
    _inherit = "uom.uom"

    alias_ids = fields.One2many(
        comodel_name="uom.alias",
        inverse_name="uom_id",
        string="Uom Alias",
    )

    @property
    def _rec_names_search(self):
        return list(set(super()._rec_names_search or [] + ["alias_ids.code"]))

    @api.model
    def search(self, domain, *args, **kwargs):
        for dom in list(filter(lambda x: x[0] == "name", domain)):
            domain = expression.OR([domain, [("alias_ids.code", dom[1], dom[2])]])
        return super().search(domain, *args, **kwargs)
