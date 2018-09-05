# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProductSecondaryUnit(models.Model):
    _name = 'product.secondary.unit'

    name = fields.Char(required=True)
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template',
        required=True,
    )
    uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='Secondary Unit of Measure',
        required=True,
        help="Default Secondary Unit of Measure.",
    )
    factor = fields.Float(
        string='Secondary Unit Factor',
        default=1.0,
        digits=0,
        required=True,
    )

    @api.multi
    def name_get(self):
        result = []
        for unit in self:
            result.append((unit.id, "{uom_to}-{factor}".format(
                uom_to=unit.uom_id.name,
                factor=unit.factor))
            )
        return result
