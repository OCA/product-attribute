#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Pricelist Rule UoM",
    "summary": "Set UoM in Pricelist Rules.",
    "version": "16.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/OCA/product-attribute"
    "/tree/16.0/product_pricelist_item_uom",
    "author": "Aion Tech, Odoo Community Association (OCA)",
    "maintainers": [
        "SirAionTech",
    ],
    "license": "AGPL-3",
    "depends": [
        "product",
        "uom",
    ],
    "data": [
        "views/product_pricelist_item_views.xml",
        "views/product_pricelist_views.xml",
    ],
}
