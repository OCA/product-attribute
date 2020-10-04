# -*- coding: utf-8 -*-
# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, fields, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = [_name, "custom.info"]

    custom_info_template_id = fields.Many2one(
        context={"default_model": _name},
    )
    custom_info_ids = fields.One2many(
        context={"default_model": _name},
    )
    product_tmpl_custom_info_ids = fields.Many2many(
        comodel_name='custom.info.value',
        compute="_compute_product_tmpl_custom_info_ids",
        string="Product template info",
    )

    @api.multi
    def _compute_product_tmpl_custom_info_ids(self):
        value_obj = self.env['custom.info.value']
        for product in self:
            product.product_tmpl_custom_info_ids = value_obj.search([
                ('res_id', '=', product.product_tmpl_id.id),
                ('model', '=', 'product.template'),
            ])

    @api.multi
    def open_product_template(self):
        # HACK: Method is duplicated on core and the second one misses this
        res = super(ProductProduct, self).open_product_template()
        res['flags'] = {'form': {'action_buttons': True}}
        return res
