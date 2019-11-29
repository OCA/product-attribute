# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    attr_type = fields.Selection([('select', 'Select'),
                                  ('range', 'Range'),
                                  ('numeric', 'Numeric')],
                                 required=True,
                                 string="Type", default='select')


class ProductAttributeLine(models.Model):
    _inherit = "product.attribute.line"

    required = fields.Boolean('Required')
    default = fields.Many2one('product.attribute.value', 'Default')
    attr_type = fields.Selection(string='Type', store=False,
                                 related='attribute_id.attr_type')


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    attr_type = fields.Selection(string='Type',
                                 related='attribute_id.attr_type', store=True)
    numeric_value = fields.Float('Numeric Value',
                                 digits=dp.get_precision('Product Attribute'))
    min_range = fields.Float('Min',
                             digits=dp.get_precision('Product Attribute'))
    max_range = fields.Float('Max',
                             digits=dp.get_precision('Product Attribute'))

    @api.constrains('min_range', 'max_range')
    def _check_min_max_range(self):
        for value in self:
            # we check only values of range type attributes.
            if value.attr_type != 'range':
                continue
            if value.min_range > value.max_range:
                raise ValidationError(
                    _('The min range should be less than the max range.'))
        return True
