# coding: utf-8
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields
from .product_attribute import SEQUENCE_ATTR_HELP


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'
    _order = 'attribute_sequence, value_sequence, name'

    attribute_sequence = fields.Integer(
        string='Sequence Attribute', oldname='priority',
        readonly=True,
        store=True,
        related='attribute_id.sequence',
        help=SEQUENCE_ATTR_HELP
    )
    value_sequence = fields.Integer(
        string='Sequence Value', default=10,
        help="Allow to sort attributes values")
