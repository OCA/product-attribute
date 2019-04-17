# -*- coding: utf-8 -*-
{
    "name": "Product Exception",
    "summary": "Ensure products are valid against a set of rules",
    "version": "10.0.1.0.0",
    "development_status": "Beta",
    "category": "Quality",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Akretion, Odoo Community Association (OCA)",
    "maintainers": ["hparfr"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
        "base_exception"
    ],
    "demo": [
        "demo/product_exception.xml",
    ],
    "data": [
        "data/data.xml",
        "views/product.xml",
    ],
}
