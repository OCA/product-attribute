# Copyright 2019- WT-IO-IT GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Product Supplierinfo UoM Rule',
    "summary": "Allows to define supplier prices for a different UoM on the price rule",
    'version': '12.0.1.0.0',
    "website": "https://github.com/OCA/product-attribute",
    "author":   "WT-IO-IT GmbH, "
                "Wolfgang Taferner, "
                "Odoo Community Association (OCA)",
    "license": 'AGPL-3',
    'installable': True,
    'category': 'Purchase',
    'depends': [
        'product'
    ],
    'data': [
        'views/product.xml',
    ],
    "demo": [
        "demo/product.xml",
    ],
}
