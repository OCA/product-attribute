# coding: utf-8
# © 2016 Abdessamad HILALI <abdessamad.hilali@akretion.com>
# © 2016 David BEAL <david.beal@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    base_code = fields.Char(
        string='Base Code',
        help="this field is used like a base to automatically create "
             "Internal Reference (default_code)")
    auto_default_code = fields.Boolean(
        string='Automatic Reference',
        default=True,
        help="Generate Reference automatically according to attributes")


class ProductProduct(models.Model):
    _inherit = "product.product"

    manual_default_code = fields.Char(
        help="Invisible field used to store default_code value")
    default_code = fields.Char(compute="_compute_default_code",
                               inverse="_set_manual_default_code",
                               store=True)

    @api.multi
    def _get_default_code(self):
        """ Used to create a list of code elements  """
        self.ensure_one()
        res = self.base_code or ''
        attributes = {}
        attrs_order = {x.attribute_id: x.attribute_id.code or ''
                       for x in self.product_tmpl_id.attribute_line_ids}
        for value in self.attribute_value_ids:
            attributes[attrs_order[value.attribute_id]] = value
        if attributes:
            order = attributes.keys()
            order.sort()
            for elm in order:
                res += ''.join([
                    attributes[elm]['attribute_id']['code'] or '',
                    attributes[elm]['code'] or ''
                ])
        return res

    def _set_manual_default_code(self):
        self.manual_default_code = self.default_code

    @api.depends('auto_default_code',
                 'attribute_value_ids.attribute_id.code',
                 'attribute_value_ids.code',
                 'product_tmpl_id.base_code')
    @api.multi
    def _compute_default_code(self):
        for record in self:
            if record.auto_default_code:
                record.default_code = record._get_default_code()
            else:
                record.default_code = record.manual_default_code
