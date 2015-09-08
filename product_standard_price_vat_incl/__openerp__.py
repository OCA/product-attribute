# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Standard Price VAT Included Module for Odoo
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
    'name': 'Product - Standard Price VAT Included',
    'version': '0.1',
    'category': 'Product',
    'description': """
This module brings an standard Price with VAT Included
======================================================

This module is interesting in the following case:
    * You use VAT With Price Included;
    * You want to create price list based on standard Price;

Without this module, the sale price (with a price list based on standard price)
will be bad, because the VAT will be not correctly computed;

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2015, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'sale_stock',
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
