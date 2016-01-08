# -*- coding: utf-8 -*-
# © 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com).
#        Pedro M. Baezr <pedro.baeza@serviciosbaeza.com>.
# © 2015 Therp BV (http://therp.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, _


FIXED_PRICE_TYPE = -3


class ProductPricelistItem(models.Model):
    """Add fixed price option to pricelist item."""
    _inherit = 'product.pricelist.item'

    def _price_field_get_ext(self):
        """Add fixed price to pricetype selection."""
        result = self._price_field_get()
        result.append((FIXED_PRICE_TYPE, _('Fixed Price')))
        return result

    base_ext = fields.Selection(
        selection='_price_field_get_ext',
        string='Based on',
        size=-1,  # Needed when selection is for integer based values.
        required=True,
        default=lambda self:
            self.default_get(
                fields_list=['base']
            )['base'],
        help="Base price for computation",
    )

    @api.constrains('base_ext')
    def _check_fixed_price(self):
        """Ensure fixed prices always refer to a specific product.

        Values for price_discount and price_round will not be checked,
        because create and write will automagically set appropiate
        values.
        """
        if self.base_ext == FIXED_PRICE_TYPE and not self.product_id:
            raise ValidationError(
                _("Product required for fixed price item.")
            )

    def _auto_end(self, cr, context=None):
        """Make sure that after updating database tables for this module,
        existing values in pricelist item are set correctly."""
        cr.execute(
            'update product_pricelist_item'
            ' set base_ext = base'
            ' where base_ext != -3 and base != base_ext'
        )
        return super(ProductPricelistItem, self)._auto_end(
            cr, context=context)

    @api.model
    def _get_fixed_price_base(self):
        """Return value to set on base when using fixed price item."""
        base = self.env['product.price.type'].search([], limit=1, order='id')
        assert base, _("No record found in product.price.type")
        return base[0].id

    @api.model
    def _modify_vals(self, vals):
        """Ensure consistent values for fixed pricelist items.

        The passed vals parameter is used for both input and output.
        base should be default if base-ext = -1, in all other cases base and
        base_ext should be the same.
        """
        # Check wether any action is needed
        if not ('base_ext' in vals or 'base' in vals):
            return
        # Get base and base_ext values
        if 'base_ext' in vals:
            base_ext = vals['base_ext']
            if base_ext != FIXED_PRICE_TYPE:
                base = base_ext
            else:
                base = self._get_fixed_price_base()
        else:
            # getting here we are sure base is in vals
            base = vals['base']
            base_ext = base
        # Synchronize base and base_ext values
        vals.update({
            'base_ext': base_ext,
            'base': base,
        })
        # Make sure other values valid for fixed price
        if base_ext == FIXED_PRICE_TYPE:
            vals.update({
                'price_discount': -1.0,
                'price_round': 0.0,
                'price_min_margin': 0.0,
                'price_max_margin': 0.0,
            })

    @api.model
    def create(self, vals):
        """override create to get computed values"""
        self._modify_vals(vals)
        return super(ProductPricelistItem, self).create(vals)

    @api.multi
    def write(self, vals):
        """override write to get computed values."""
        self._modify_vals(vals)
        return super(ProductPricelistItem, self).write(vals)

    @api.onchange('base_ext')
    def change_base_ext(self):
        if self.base_ext == FIXED_PRICE_TYPE:
            self.base = self._get_fixed_price_base()
            self.price_discount = -1
            self.price_round = 0.0
            self.price_min_margin = 0.0
            self.price_max_margin = 0.0
        else:
            self.base = self.base_ext
            if self.price_discount == -1.0:
                # Reset fixed price discount
                self.price_discount = 0.0
