# Copyright 2017 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    show_in_simulation = fields.Boolean(string="Show in simulation")
