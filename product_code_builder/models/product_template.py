# coding: utf-8
# © 2016 Abdessamad HILALI <abdessamad.hilali@akretion.com>
# © 2016 David BEAL <david.beal@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def compute_default_auto_default_code(self):
        if self._context.get('module') == 'product_code_builder':
            # When we install the module we return False for the existing
            # record
            return False
        return True

    prefix_code = fields.Char(
        string='Internal Reference',
        help="This is the code of the product model"
             "If Automatic Reference is checked, "
             "this field is used as a prefix for "
             "the product variant reference.\n"
             "In case that there is only one variant "
             "this code is the same as the code of the uniq variant")
    default_code = fields.Char(related='prefix_code')
    auto_default_code = fields.Boolean(
        string='Automatic Reference',
        default=compute_default_auto_default_code,
        help="Generate a reference automatically "
             "based on attribute codes")

    _sql_constraints = [
        ('uniq_prefix_code',
         'unique(prefix_code)',
         'The reference must be unique'),
    ]
