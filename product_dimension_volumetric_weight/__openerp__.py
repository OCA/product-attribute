# -*- coding: utf-8 -*-
# © 2015 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Dimension: Volumetric Weight",
    "summary": "Adds a new computed field in product containing the "
    "volumetric weight",
    "version": "8.0.1.0.0",
    "category": "Product",
    "website": "https://factorlibre.com/",
    "author": "FactorLibre, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
        "product_dimension",
    ],
    "data": [
        "views/product_view.xml"
    ]
}
