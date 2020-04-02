# Copyright (C) 2014 GRAP (http://www.grap.coop)
# Copyright (C) 2019-Today: Druidoo (<https://www.druidoo.io>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductScaleSystemProductLine(models.Model):
    _name = 'product.scale.system.product.line'
    _order = 'scale_system_id, sequence'
    _description = 'Product Scale System Product'

    _TYPE_SELECTION = [
        ('id', 'Product ID'),
        ('numeric', 'Numeric Field'),
        ('text', 'Char / Text Field'),
        ('external_text', 'External Text Field'),
        ('constant', 'Constant Value'),
        ('external_constant', 'External Constant Text Value'),
        ('many2one', 'ManyOne Field'),
        ('many2many', 'Many2Many Field'),
        ('product_image', 'Product Image'),
    ]

    # Column Section
    scale_system_id = fields.Many2one(
        'product.scale.system',
        'Scale System',
        required=True,
        ondelete='cascade', index=True
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='scale_system_id.company_id'
    )
    code = fields.Char('Bizerba Code', required=True)
    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', required=True, default=10)
    type = fields.Selection(_TYPE_SELECTION, string='Type')
    field_id = fields.Many2one(
        'ir.model.fields',
        string='Product Field',
        domain=[('model', 'in', ['product.product', 'product.template'])]
    )
    related_field_id = fields.Many2one(
        'ir.model.fields',
        string='M2M / M2O Field',
        help="Used only"
        " for the x2x fields. Set here the field of the related model"
        " that you want to send to the scale. Let empty to send the ID."
    )
    x2many_range = fields.Integer(
        'range of the x2Many Fields',
        help="Used if type is"
        " 'Many2Many Field', to mention the"
        " range of the field  to send. Begin by 0. (used for exemple"
        " for product logos)"
    )
    constant_value = fields.Char(
        'Constant Value',
        help="Used if type is 'constant',"
        " to send allways the same value."
    )
    multiline_length = fields.Integer(
        'Length for Multiline',
        help="Used if type is 'Text Field' or 'External Text Constant'"
        ", to indicate the max length of a line. Set 0 to avoid to split"
        " the value.",
        default=0
    )
    multiline_separator = fields.Char(
        'Separator for Multiline',
        help="Used if type is"
        " 'Text Field' or 'External Text Constant', to indicate wich text"
        " will be used to mention break lines.",
        default='\n'
    )
    suffix = fields.Char(
        'Suffix',
        help="Used if type is"
        " 'External Text Field', to indicate how to suffix the field.\n"
        " Make sure to have a uniq value by Scale System, and all with the"
        " same size.\n\n Used if type is Product Image to mention the end"
        " of the file. Exemple : '_01.jpg'."
    )
    numeric_coefficient = fields.Float(
        'Numeric Coefficient',
        help="Used if type is"
        " 'Numeric Field', to mention with coefficient numeric"
        " field should be multiplyed.",
        default=1.00
    )
    numeric_round = fields.Float(
        'Rounding Method',
        help="Used if type is"
        " 'Numeric Field', to mention how the value should be rounded.\n"
        " Do not Use 0, because it will truncate the value.",
        default=1.00
    )
    delimiter = fields.Char(
        'Delimiter Char',
        help="Used to finish the column",
        default='#'
    )
