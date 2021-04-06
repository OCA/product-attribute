# Copyright 2020 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductApplication(models.Model):
    _name = 'product.application'

    name = fields.Char('Application Name', required=True)

    product_tmpl_ids = fields.Many2many(
        comodel_name='product.template',
        relation='product_template_application_rel',
        column1='application_id',
        column2='product_tmpl_id',
        string='Product Templates',
    )

    # FIXME: Delete field product_tmpl_id:
    @api.model
    def _default_product_template(self):
        product_obj = self.env['product.product']

        if self._context.get('default_template_id', False):
            return self._context['default_template_id']
        elif self._context.get('default_product_id', False):
            product = product_obj.browse(self._context['default_product_id'])
            return product.product_tmpl_id.id
        return 0

    product_tmpl_id = fields.Many2one(
        'product.template',
        'Product Template',
        help="Product Template",
        required=False,
        default=_default_product_template
    )
