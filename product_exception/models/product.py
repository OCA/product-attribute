# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# @author Raphaël Reverdy <raphael.reverdy@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = ['product.template', 'base.exception']
    _name = 'product.template'

    @api.model
    def check_product_template_cron(self):
        products = self.env['product.template'].search([])
        products.detect_exceptions()

    @api.multi
    def check_exception(self):
        if self.detect_exceptions():
            return self._popup_exceptions()

    @api.model
    def _reverse_field(self):
        return 'product_tmpl_ids'


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def check_exception(self):
        """Shortcut from variant view."""
        return self.product_tmpl_id.check_exception()
