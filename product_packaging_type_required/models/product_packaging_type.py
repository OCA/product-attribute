# Copyright 2019 Camptocamp (<http://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class ProductPackagingType(models.Model):
    _inherit = "product.packaging.type"

    required = fields.Boolean()

    @api.model
    def cron_check_create_required_packaging(self, limit=0):
        """ if limit=0, the method will not apply a limit to process missing
        packages.
        """
        existing_products = self.env['product.product'].search(
            [('type', 'in', ('product', 'consu'))]
        )
        i = 0
        for p_type in self.search([('required', '=', True)]):
            if limit and i == limit:
                break
            for product in existing_products:
                packaging = self.env['product.packaging'].search(
                    [('product_id', '=', product.id),
                     ('packaging_type_id', '=', p_type.id)]
                )
                if packaging:
                    continue
                else:
                    packaging.create(
                        p_type.prepare_packaging_vals(product)
                    )
                    i += 1
        return True

    def prepare_packaging_vals(self, product):
        self.ensure_one()
        res = {
            'packaging_type_id': self.id,
            'name': self.name,
            'product_id': product.id,
        }
        return res
