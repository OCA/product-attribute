# -*- encoding: utf-8 -*-
###############################################################################
# #                                                                           #
# product_feature for Odoo                                                    #
# Copyright (C) 2016 Rubén Cabrera Martínez                                   #
# Copyright (C) 2016 Praxya Soluciones                                        #
# #                                                                           #
# This program is free software: you can redistribute it and/or modify #      #
# it under the terms of the GNU Affero General Public License as #            #
# published by the Free Software Foundation, either version 3 of the #        #
# License, or (at your option) any later version. #                           #
# #                                                                           #
# This program is distributed in the hope that it will be useful, #           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of #            #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the #              #
# GNU Affero General Public License for more details. #                       #
# #                                                                           #
# You should have received a copy of the GNU Affero General Public License #  #
# along with this program. If not, see <http://www.gnu.org/licenses/>. #      #
# #                                                                           #
###############################################################################
###############################################################################
# Product Feature is an Odoo module wich enables Feature management for       #
# products                                                                    #
###############################################################################
from openerp import models, fields, api, _


class ProductFeature(models.Model):
    _name = 'product.feature'

    name = fields.Char('Feature Name', required=True)
    description = fields.Text('Description', translate=True)
    image = fields.Binary('Image File')
    alt_text = fields.Char(
        string=_('Alt text'),
        help=_('Text to be displayed on image loading failure'),
    )
    product_ids = fields.Many2many(
        'product.template',
        string='Products',
    )


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    feature_ids = fields.Many2many(
        'product.feature',
        string='Features',
        help='Select features for this product'
    )
