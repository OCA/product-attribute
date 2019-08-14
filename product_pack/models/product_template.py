# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pack_type = fields.Selection([
        ('components_price', 'Detailed - Components Prices'),
        ('totalized_price', 'Detailed - Totalized Price'),
        ('fixed_price', 'Detailed - Fixed Price'),
        ('none_detailed_totalized_price', 'None Detailed - Totalized Price'),
    ],
        'Pack Type',
        help="On sale orders or purchase orders:\n"
             "* Detailed - Components Prices: Detail lines with prices.\n"
             "* Detailed - Totalized Price: Detail lines totalicing "
             "lines prices on pack (don't show component prices).\n"
             "* Detailed - Fixed Price: Detail lines and use product"
             " pack price (ignore line prices).\n"
             "* None Detailed - Totalized Price: Do not detail lines. "
             "Do not assist to get pack price using pack lines."
    )
    pack_ok = fields.Boolean(
        'Is Pack?',
        help='Is a Product Pack?',
    )
    pack_line_ids = fields.One2many(
        related='product_variant_ids.pack_line_ids',
    )
    used_in_pack_line_ids = fields.One2many(
        related='product_variant_ids.used_in_pack_line_ids',
        readonly=True,
    )
    pack_modifiable = fields.Boolean()

    @api.onchange('pack_type')
    def onchange_pack_type(self):
        products = self.filtered(
            lambda x: x.pack_modifiable and
            x.pack_type and x.pack_type != 'components_price')
        for rec in products:
            rec.pack_modifiable = False

    @api.constrains('company_id', 'product_variant_ids')
    def _check_pack_line_company(self):
        """Check packs are related to packs of same company."""
        for rec in self:
            for line in rec.pack_line_ids:
                if (line.product_id.company_id and rec.company_id) and \
                        line.product_id.company_id != rec.company_id:
                    raise ValidationError(_(
                        'Pack lines products company must be the same as the '
                        'parent product company'))
            for line in rec.used_in_pack_line_ids:
                if (line.product_id.company_id and rec.company_id) and \
                        line.parent_product_id.company_id != rec.company_id:
                    raise ValidationError(_(
                        'Pack lines products company must be the same as the '
                        'parent product company'))

    @api.multi
    def write(self, vals):
        """We remove from product.product to avoid error."""
        _vals = vals.copy()
        if vals.get('pack_line_ids', False):
            self.product_variant_ids.write(
                {'pack_line_ids': vals.get('pack_line_ids')})
            _vals.pop('pack_line_ids')
        return super().write(_vals)
