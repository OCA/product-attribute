# Copyright 2026 AGF Vector GmbH (<https://agfvector.at>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product State Restriction",
    "summary":"""
    """,
    "author": "AGF Vector GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "version": "19.0.1.0.0",
    "category": "Product",
    "depends": [
        "product_state",
        "product_state_sale",
        "sale",        
        "mrp",         
        "stock",
    ],
    "data": [
        "views/product_state_views.xml",
    ],
    "application": False,
    "maintainers": ["flogruber"],
    "license": "AGPL-3",
}