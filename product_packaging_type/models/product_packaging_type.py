# Copyright 2019 Camptocamp (<http://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from collections import OrderedDict
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductPackagingType(models.Model):
    _name = "product.packaging.type"
    _description = "Type management for product.packaging"
    _order = 'sequence, code'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True)
    sequence = fields.Integer(required=True)
    has_gtin = fields.Boolean()
    active = fields.Boolean(default=True)
    is_default = fields.Boolean()

    @api.constrains('is_default')
    def _check_is_default(self):
        msg = False
        default_count = self.search_count([('is_default', '=', True)])
        if default_count == 0:
            msg = _(
                'There must be one product packaging type set as "Is Default".'
            )
        elif default_count > 1:
            msg = _(
                'Only one product packaging type can be set as "Is Default".'
            )
        if msg:
            raise ValidationError(msg)


class ProductPackaging(models.Model):
    _inherit = "product.packaging"
    _order = 'product_id, type_sequence'

    @api.model
    def default_packaging_type_id(self):
        return self.env['product.packaging.type'].search(
            [('is_default', '=', True)], limit=1
        )

    packaging_type_id = fields.Many2one(
        "product.packaging.type",
        required=True,
        ondelete="restrict",
        default=lambda p: p.default_packaging_type_id(),
    )
    type_has_gtin = fields.Boolean(related="packaging_type_id.has_gtin",
                                   readonly=True)
    type_sequence = fields.Integer(
        string="Type sequence",
        related="packaging_type_id.sequence",
        readonly=True,
        store=True,
    )
    qty_per_type = fields.Html(
        compute='_compute_qty_per_type', string='Qty per package type',
    )

    @api.depends(
        'product_id', 'product_id.packaging_ids', 'packaging_type_id',
        'packaging_type_id.code'
    )
    def _compute_qty_per_type(self):
        for packaging in self:
            product = packaging.product_id
            if not product:
                continue

            smaller_product_packagings = product.packaging_ids.filtered(
                lambda p: p.id != packaging.id and p.qty < packaging.qty
            )
            res = OrderedDict()
            for p_pack in smaller_product_packagings.sorted(
                lambda p: p.qty
            ):
                res[p_pack.packaging_type_id.code] = p_pack.qty
            packaging.qty_per_type = packaging._format_qty_per_type(res)

    def _format_qty_per_type(self, qty_per_type_dict):
        self.ensure_one()
        res = []
        for code, qty in qty_per_type_dict.items():
            new_qty = self.qty / qty
            if not new_qty.is_integer():
                new_qty_int = int(new_qty)
                new_qty_decimals = new_qty - new_qty_int
                new_qty = '%s<span style="color: red;">%s</span>' % (
                    new_qty_int, str(new_qty_decimals).lstrip('0')
                )
            res.append('%s %s' % (new_qty, code))
        return '; '.join(res)
