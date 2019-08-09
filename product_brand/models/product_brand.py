# Copyright 2009 NetAndCo (<http://www.netandco.net>).
# Copyright 2011 Akretion Benoît Guillot <benoit.guillot@akretion.com>
# Copyright 2014 prisnet.ch Seraphine Lantible <s.lantible@gmail.com>
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# Copyright 2018 Daniel Campos <danielcampos@avanzosc.es>
# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.exceptions import ValidationError
from odoo import api, fields, models, _


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = "Product Brand"
    _order = 'name'

    name = fields.Char('Brand Name', required=True)
    description = fields.Text(translate=True)
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Select a partner for this brand if any.',
        ondelete='restrict'
    )
    logo = fields.Binary('Logo File', attachment=True)
    product_ids = fields.One2many(
        'product.template',
        'product_brand_id',
        string='Brand Products',
    )
    products_count = fields.Integer(
        string='Number of products',
        compute='_compute_products_count',
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'product.brand'
        ),
        ondelete='restrict',
    )

    @api.multi
    @api.depends('product_ids')
    def _compute_products_count(self):
        for brand in self:
            brand.products_count = len(brand.product_ids)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_brand_id = fields.Many2one(
        'product.brand',
        string='Brand',
        help='Select a brand for this product'
    )

    @api.constrains('company_id', 'product_brand_id')
    def _check_product_brand_company(self):
        for product in self:
            if (
                product.company_id
                and product.product_brand_id.company_id
                and product.company_id != product.product_brand_id.company_id
            ):
                raise ValidationError(
                    _('Product and brand must be related to the same company')
                )
