#  Copyright 2023 Francesco Ballerini
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Pricelist Percent Change Supplier Info",
    "version": "14.0.0.0.1",
    "category": "Product",
    "summary": """
        Enable percentage change computation for pricelist items
        based on supplierinfo price.
    """,
    "author": "Francesco Ballerini, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "support": "francescobl.lavoro@gmail.com",
    "depends": [
        "product_form_pricelist_percent_change",
        "product_pricelist_supplierinfo",
    ],
    "data": [],
    "application": False,
    "installable": True,
    "license": "AGPL-3",
}
