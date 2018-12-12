# -*- coding: utf-8 -*-
# Copyright 2015 Sergio Teruel <sergio.teruel@tecnativa.com>
# Copyright 2015 Carlos Dauden <carlos.dauden@tecnativa.com>
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from openerp import fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = [_name, "custom.info"]

    custom_info_template_id = fields.Many2one(
        context={"default_model": _name})
    custom_info_ids = fields.One2many(
        context={"default_model": _name})
