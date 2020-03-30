# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError
from odoo.addons import decimal_precision as dp


class ProductMultiPrice(models.Model):
    _name = 'product.multi.price'

    name = fields.Many2one(
        comodel_name='product.multi.price.name',
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        required=True,
        ondelete='cascade',
    )
    price = fields.Float(
        digits=dp.get_precision('Product Price'),
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        related='name.company_id',
        store=True,
        readonly=True,
    )

    _sql_constraints = [
        ('multi_price_uniq', 'unique(name, product_id, company_id)',
         'A field name cannot be assigned to a product twice for the same '
         'company'),
    ]


class ProductMultiPriceName(models.Model):
    _name = 'product.multi.price.name'

    @api.model
    def _get_company(self):
        return self._context.get('company_id', self.env.user.company_id.id)

    name = fields.Char(
        required=True,
        string='Price Field Name',
        ondelete='restrict'
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True,
        default=lambda self: self._get_company()
    )

    _sql_constraints = [
        ('multi_price_name_uniq', 'unique(name, company_id)',
         'Prices Names must be unique per company'),
    ]

    @api.model
    @tools.ormcache()
    def _get_field_names(self):
        return set([x.name for x in self.search([])])

    @api.model
    def create(self, vals):
        res = super().create(vals)
        self.clear_caches()
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'name' in vals:
            self.clear_caches()
        return res

    def unlink(self):
        res = super().unlink()
        self.clear_caches()
        return res

    @api.constrains('name')
    def _check_name(self):
        """The target is to use multi price as if they were virtual fields
           so we want to constrain the naming to the same rules"""
        product_fields = list(self.env['product.product']._fields)
        product_fields += list(self.env['product.template']._fields)
        for field in self:
            try:
                models.check_pg_name(field.name)
            except ValidationError:
                msg = _(
                    "Field names can only contain characters, "
                    "digits and underscores (up to 63).")
                raise ValidationError(msg)
            if field in set(product_fields):
                raise ValidationError(_(
                    "The field name is used in the model, try another"))
