# coding: utf-8
# © 2015 Benoît GUILLOT <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    code = fields.Char('Code')
    sequence = fields.Integer('Sequence')

    _sql_constraints = [
        ('attr_code_uniq', 'unique(code)',
         "With each Attribute we must be found a unique 'code'"),
    ]


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    _code = "code"
    _order = "attribute_sequence,sequence,name"

    code = fields.Char('Code')
    comment = fields.Text('Comment')
    attribute_sequence = fields.Integer(
        related="attribute_id.sequence",
        store=True)

    _sql_constraints = [
        ('attr_val_code_uniq', 'unique(code, attribute_id)',
         "For each Attribute we must be found a unique 'code'"),
        ]
