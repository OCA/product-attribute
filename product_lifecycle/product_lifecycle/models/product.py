# Copyright 2019 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models, fields, api


class ProductProduct(models.Model):

    _inherit = 'product.product'
    replace_to_product_ids = fields.One2many(
        'product.product',
        'replaced_by_product_id',
        string='Replace To',
        help="Informative field. The product that is replaced by the"
             " current one. The current product is the new product for"
             " the product in this field")

    replaced_by_product_id = fields.Many2one(
        'product.product',
        string='Replaced By',
        help="The replacement product for the current product."
             " The current product is a obsolete product and the product"
             " in this field is the new product that make the replacement")

    lifecycle_state = fields.Selection([
        ('normal', 'Normal'),
        ('end', 'End of Lifecycle'),
        ('obsolete', 'Obsolete')], default='normal', string='State', copy=False)

    @api.multi
    def get_good_replacements(self):
        """:return: the replace by product (new product) if the product is not
                 obsolete and is and active product.
        """
        self.ensure_one()
        replace = self.replaced_by_product_id
        if not replace or (replace.lifecycle_state != 'obsolete' and replace.active):
            return replace
        return replace.get_good_replacements()

    @api.multi
    def write(self, values):
        """ Try to set the lifecycle_state to obsolete when quantity on hand will change
        the product to end instead.
        """
        for product in self:
            lc_state = values.get('lifecycle_state', product.lifecycle_state)
            available = values.get('virtual_available', product.virtual_available)

            if lc_state == 'obsolete' and available:
                values.update({'lifecycle_state': 'end'})
            elif lc_state == 'end' and not available:
                values.update({'lifecycle_state': 'obsolete'})
            super(ProductProduct, product).write(values)
        return True

    def update_product_state(self):
        """ Check the product state
            - if in end state but has not inventory then pass to obsolete.
            - if obsolete but with inventory pass to end of life.
        """
        end_product = self.search([('lifecycle_state', '=', 'obsolete')]).filtered(
            lambda product: product.qty_available)

        obsolete_product = self.search([('lifecycle_state', '=', 'end')]).filtered(
            lambda product: not product.qty_available)

        end_product.write({'lifecycle_state': 'end'})
        obsolete_product.write({'lifecycle_state': 'obsolete'})
