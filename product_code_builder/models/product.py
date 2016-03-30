# coding: utf-8
# © 2016 Abdessamad HILALI <abdessamad.hilali@akretion.com>
# © 2016 David BEAL <david.beal@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    prefix_code = fields.Char(
        string='Internal Reference',
        help="Code of the product.\nIf Automatic Reference is checked, "
             "this field is used as prefix of the Internal Reference "
             "of the product variant")
    auto_default_code = fields.Boolean(
        string='Automatic Reference',
        default=True,
        help="Generate Internal Reference automatically "
             "according to attribute codes")


class ProductProduct(models.Model):
    _inherit = "product.product"

    default_code = fields.Char(compute="_compute_default_code", store=True)

    @api.multi
    def _get_default_code(self):
        """ Used to create a list of code elements """
        self.ensure_one()
        res = self.prefix_code or ''
        attributes = {}
        attrs_order = self._get_attribute_order()
        for value in self.attribute_value_ids:
            attributes[attrs_order[value.attribute_id]] = value
        if attributes:
            order = attributes.keys()
            order.sort()
            # order contains values from attrs_order
            for elm in order:
                res += ''.join([
                    attributes[elm]['attribute_id']['code'] or '',
                    attributes[elm]['code'] or ''
                ])
        return res

    @api.multi
    def _get_attribute_order(self):
        """ Return a dict {attribute_id: value} in which value
            will be used as attribute to define order
            to create default_code with attribute """
        self.ensure_one()
        # you can inherit to switch another value
        return {x.attribute_id: (str(x.attribute_id.sequence) or '' +
                                 x.attribute_id.code or '')
                for x in self.product_tmpl_id.attribute_line_ids}

    @api.depends('auto_default_code',
                 'attribute_value_ids.attribute_id.code',
                 'attribute_value_ids.code',
                 'product_tmpl_id.prefix_code')
    @api.multi
    def _compute_default_code(self):
        for record in self:
            print 'default_code', record.default_code, record.auto_default_code
            if record.auto_default_code:
                record.default_code = record._get_default_code()
            elif not record.default_code:
                record.default_code = record.prefix_code
                print 'default_code', record.default_code
