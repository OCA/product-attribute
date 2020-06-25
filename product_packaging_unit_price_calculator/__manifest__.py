# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Product Packaging Unit Price Calculator",
    "summary": "",
    "version": "13.0.1.0.0",
    "category": "Product",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["product"],
    "website": "https://www.camptocamp.com",
    "data": [
        "views/product_view.xml",
        "views/product_supplierinfo.xml",
        "views/product_packaging.xml",
        "views/product_pricelist.xml",
        "wizards/product_package_price.xml",
    ],
    "installable": True,
}
