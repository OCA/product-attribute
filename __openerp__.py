# -*- encoding: utf-8 -*-
##############################################################################
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
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
{
    "name": "Product Variant Default Code",
    "version": "2.0",
    "author": "Shine IT(http:www.openerp.cn), OdooMRP team",
    "contributors": "Tony Gu<tony@openerp.cn>",
    "category": "Product",
    "website": "http://www.odoomrp.com",
    "description": """
    This module adds:

    1.- In 'product.template' object 'variant_reference mask' field is added

    2.- In 'product.attribute.value' object is added the new field
        'Attribute Code'.

    3.- Reference mask is automatically created according to the attribute 
        line settings on the product template. The mask can be changed
        adaptively later on and the default code for vaiants will be
        generated accodingly.

    4.- Reference code field of product is calculated automatically, taking as
        the value of the new field 'Attribute Code'.
    """,
    "depends": ['product',
                ],
    "data": ['views/product_attribute_value_view.xml',
             'views/product_view.xml',
             ],
    "installable": True
}
