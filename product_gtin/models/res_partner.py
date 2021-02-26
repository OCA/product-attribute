# © 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'abstract.ean']

    @api.constrains('barcode')
    def _check_barecode(self):
        if self.barcode:
            self._check_code(self.barcode)
