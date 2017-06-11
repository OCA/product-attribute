# coding: utf-8
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields
from .product_attribute import SEQUENCE_ATTR_HELP


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'
    _order = 'attribute_sequence, sequence, name'

    attribute_sequence = fields.Integer(
        string='Attribute Sequence', oldname='priority',
        readonly=True,
        store=True,
        related='attribute_id.sequence',
        help=SEQUENCE_ATTR_HELP
    )
