# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        if self.categ_id and self.categ_id.restricted_product_type:
            self.type = self.categ_id.restricted_product_type

    @api.onchange('type')
    def _onchange_type(self):
        if self.type:
            return {'domain': {'categ_id': [
                ('restricted_product_type', 'in', [self.type, False])]}}
        else:
            return {'domain': {'categ_id': []}}

    @api.constrains("type")
    def _check_product_type(self):
        for product in self:
            if product.categ_id.restricted_product_type and product.type != \
                    product.categ_id.restricted_product_type:
                    raise ValidationError(_(
                        'The product type must be equal to the restricted '
                        'product type defined in the product category'))
