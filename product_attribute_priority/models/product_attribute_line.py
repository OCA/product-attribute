# coding: utf-8
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields
from .product_attribute import SEQUENCE_ATTR_HELP


class ProductAttributeLine(models.Model):

    _inherit = 'product.attribute.line'
    _order = 'attribute_sequence'

    attribute_sequence = fields.Integer(
        string='Priority', oldname='priority',
        readonly=True,
        store=True,
        related='value_ids.sequence',
        help=SEQUENCE_ATTR_HELP
    )
