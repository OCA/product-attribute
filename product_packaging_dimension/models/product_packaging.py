# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    max_weight = fields.Float('Weight (kg)')
    # lngth IS NOT A TYPO https://github.com/odoo/odoo/issues/41353
    lngth = fields.Integer("Length (mm)", help="length in millimeters")
    width = fields.Integer('Width (mm)', help='width in millimeters')
    height = fields.Integer('Height (mm)', help='height in millimeters')
    volume = fields.Float(
        'Volume (m³)',
        digits=(8, 4),
        compute='_compute_volume',
        readonly=True,
        store=False,
        help='volume in cubic meters',
    )

    @api.depends('lngth', 'width', 'height')
    def _compute_volume(self):
        for pack in self:
            pack.volume = (
                pack.lngth * pack.width * pack.height
            ) / 1000.0 ** 3
