# coding: utf-8
# © 2016 Abdessamad HILALI <abdessamad.hilali@akretion.com>
# © 2016 David BEAL <david.beal@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


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


class ProductProduct(models.Model):
    _inherit = "product.product"

    default_code = fields.Char(
        help="Reference of the variant",
        compute="_compute_default_code",
        inverse="_inverse_default_code",
        store=True,
    )

    manual_default_code = fields.Char(
        help='hidden field'
    )

    @api.multi
    def _get_default_code(self):
        """A default_code based on tmpl.prefix and attributes values.

        Return: (string)
        """
        self.ensure_one()
        res = self.prefix_code or ''
        # Invalidate cache of the product to be sure to reload the
        # attribue_value_ids with the right order
        self.env['product.product'].invalidate_cache(
            ['attribute_value_ids'], [self.id])
        for value in self.attribute_value_ids:
            res += ''.join([value.attribute_id.code or '', value.code or ''])
        return res

    @api.depends('product_tmpl_id.auto_default_code',
                 'attribute_value_ids.attribute_id.code',
                 'attribute_value_ids.attribute_sequence',
                 'attribute_value_ids.code',
                 'product_tmpl_id.prefix_code')
    @api.multi
    def _compute_default_code(self):
        for record in self:
            if record.with_context(active_test=False)\
                    .product_variant_count <= 1:
                record.default_code = record.prefix_code
            elif record.auto_default_code:
                record.default_code = record._get_default_code()
            else:
                record.default_code = record.manual_default_code

    @api.multi
    def _inverse_default_code(self):
        for record in self:
            if record.with_context(active_test=False)\
                    .product_variant_count <= 1:
                record.prefix_code = record.default_code
            elif not record.auto_default_code:
                record.manual_default_code = record.default_code
            else:
                raise UserError(
                    _('Default can no be set manually as the product '
                      'is configured to have a computed code'))
