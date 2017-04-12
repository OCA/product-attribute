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
