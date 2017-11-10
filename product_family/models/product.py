# -*- coding: utf-8 -*-
# (c) 2017 Consultoría Informática Studio73 SL (contacto@studio73.es)
#          Pablo Fuentes <pablo@studio73.es>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    family_ids = fields.Many2many(comodel_name="product.family",
                                  relation="product_tmpl_family_rel",
                                  column1="product_id", column2="family_id",
                                  string="Product Family")
