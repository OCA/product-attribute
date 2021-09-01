# Copyright 2021 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product List Pricelist Price",
    "summary": "Display pricelist prices for products in list view.",
    "version": "13.0.1.0.1",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "ForgeFlow, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["sale_management", "stock"],
    "data": [
        "views/product_template_views.xml",
        "views/product_views.xml",
        "views/product_pricelist_views.xml",
    ],
}
