# -*- coding: utf-8 -*-
#    Daniel Campos (danielcampos@avanzosc.es) Date: 08/10/2014
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Pricelist Import",
    "version": "8.0.1.0.0",
    "author": "OdooMRP team,"
              "AvanzOSC,"
              "Serv. Tecnol. Avanzados - Pedro M. Baeza",
    'website': "http://www.odoomrp.com",
    "depends": ['purchase'],
    "category": "Manufacturing",
    "data": ['wizard/import_price_file_view.xml',
             'views/product_pricelist_load_line_view.xml',
             'views/product_pricelist_load_view.xml',
             'security/ir.model.access.csv'
             ],
    "installable": True
}
