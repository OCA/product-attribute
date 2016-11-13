# coding: utf-8
# © 2015 Benoît GUILLOT <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    code = fields.Char('Code')

    _sql_constraints = [
        ('attr_code_uniq', 'unique(code)',
         "With each Attribute we must be found a unique 'code'"),
    ]
