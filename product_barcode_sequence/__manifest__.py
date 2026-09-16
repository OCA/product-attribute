# Copyright 2026 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Barcode Sequence",
    "version": "17.0.1.0.0",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "category": "Product",
    "summary": "Automatically assign EAN barcodes to products by category",
    "depends": ["product", "stock"],
    "data": [
        "views/product_category.xml",
        "data/ir_actions_server.xml",
    ],
    "installable": True,
}
