# -*- coding: utf-8 -*-
##############################################################################
#
#    Product - Cost Price Tax Included Module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Product - Cost Price Tax Included',
    'version': '8.0.1.0.0',
    'category': 'Product',
    'summary': 'Brings a Cost Price Field Tax Included on Product Model',
    'author': 'GRAP,Odoo Community Association (OCA)',
    'website': 'http://www.odoo-community.org',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'sale',
        'account',
    ],
    'data': [
        'data/product_price_type.yml',
        'view/view.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
        'demo/product_pricelist.yml',
        'demo/res_partner.yml',
        'demo/account_tax.yml',
        'demo/product_template.yml',
    ],
}
