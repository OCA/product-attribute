# Copyright (C) 2014 GRAP (http://www.grap.coop)
# Copyright (C) 2019-Today: Druidoo (<https://www.druidoo.io>)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class ProductProduct(models.Model):
    _inherit = 'product.product'

    scale_group_id = fields.Many2one(
        'product.scale.group',
        string='Scale Group',
        related="product_tmpl_id.scale_group_id",
        store=True,
        readonly=False
    )
    scale_sequence = fields.Integer('Scale Sequence',
        related="product_tmpl_id.scale_sequence",
        readonly=False,
        store=True)
    scale_tare_weight = fields.Float(
        digits=dp.get_precision('Stock Weight'),
        string='Scale Tare Weight',
        related="product_tmpl_id.scale_tare_weight",
        readonly=False,
        store=True,
        help="Set here Constant tare weight"
        " for the given product. This tare will be substracted when"
        " the product is weighted. Usefull only for weightable product.\n"
        "The tare is defined with kg uom."
    )

    # View Section
    @api.multi
    def send_scale_create(self):
        for product in self:
            self._send_to_scale_bizerba('create', product)
        return True

    @api.multi
    def send_scale_write(self):
        for product in self:
            self._send_to_scale_bizerba('write', product)
        return True

    @api.multi
    def send_scale_unlink(self):
        for product in self:
            self._send_to_scale_bizerba('unlink', product)
        return True

    # Custom Section
    @api.multi
    def _send_to_scale_bizerba(self, action, product):
        log_obj = self.env['product.scale.log']
        log_obj.create({
            'log_date': datetime.now(),
            'scale_system_id': product.scale_group_id.scale_system_id.id,
            'product_id': product.id,
            'action': action,
            })

    @api.multi
    def _check_vals_scale_bizerba(self, vals, product):
        system = product.scale_group_id.scale_system_id
        system_fields = [x.name for x in system.field_ids]
        vals_fields = list(vals.keys())
        return set(system_fields).intersection(vals_fields)

    # Overload Section
    @api.model
    def create(self, vals):
        send_to_scale = vals.get('scale_group_id', False)
        res = super(ProductProduct, self).create(vals)
        if send_to_scale:
            self._send_to_scale_bizerba('create', res)
        return res

    @api.multi
    def write(self, vals):
        defered = {}
        context = self.env.context
        ctx = context.copy()
        if not context.get('bizerba_off', False):
            for product in self:
                ignore = not product.scale_group_id\
                    and 'scale_group_id' not in list(vals.keys())
                if not ignore:
                    is_continue = False
                    if not product.available_in_pos and \
                            'available_in_pos' not in vals:
                        is_continue = True
                    if product.available_in_pos and\
                            'available_in_pos' in vals and\
                            not vals.get('available_in_pos'):
                        is_continue = True

                    if is_continue:
                        defered[product.id] = 'unlink'
                        continue
                    if not product.scale_group_id:
                        # (the product is new on this group)
                        defered[product.id] = 'create'
                    else:
                        if vals.get('scale_group_id', False) and (
                                vals.get('scale_group_id', False) !=
                                product.scale_group_id):
                            # (the product has moved from a group to another)
                            # Remove from obsolete group
                            self._send_to_scale_bizerba('unlink', product)
                            # Create in the new group
                            defered[product.id] = 'create'
                        elif self._check_vals_scale_bizerba(vals, product):
                            # Data related to the scale
                            defered[product.id] = 'write'
                        elif vals.get('available_in_pos'):
                            defered[product.id] = 'create'

        ctx['bizerba_off'] = True
        res = super(ProductProduct, self).write(vals)

        for product_id, action in defered.items():
            product = self.filtered(lambda p: p.id == product_id)
            if not product:
                continue
            self._send_to_scale_bizerba(action, product)

        return res

    @api.multi
    def unlink(self):
        for product in self:
            if product.scale_group_id:
                self._send_to_scale_bizerba('unlink', product)
        return super(ProductProduct, self).unlink()
