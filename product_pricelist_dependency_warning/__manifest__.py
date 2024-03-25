#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Pricelist Dependency Warning",
    "summary": "Warn when a dependency pricelist is updated.",
    "version": "16.0.1.0.0",
    "author": "Aion Tech, Odoo Community Association (OCA)",
    "maintainers": [
        "SirAionTech",
    ],
    "license": "AGPL-3",
    "website": "https://github.com/OCA/product-attribute"
    "/tree/16.0/product_pricelist_dependency_warning",
    "category": "Product",
    "depends": [
        "product",
    ],
    "data": [
        "views/product_pricelist_item_views.xml",
        "views/product_pricelist_views.xml",
    ],
}
