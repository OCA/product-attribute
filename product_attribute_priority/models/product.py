# coding: utf-8
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields

SEQUENCE_HELP = ("Set the display order of the attributes in backoffice "
                 "and reports")
SEQUENCE_ATTR_HELP = SEQUENCE_HELP + " (defined in Product Attribute)"


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'
    _order = 'sequence, name'

    sequence = fields.Integer(
        string='Sequence', oldname='priority', default=10,
        help=SEQUENCE_HELP)


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
