#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Price from company pricelist",
    "summary": "Manage product prices from a pricelist configured at company level.",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute"
    "/tree/16.0/product_pricelist_company_price",
    "author": "Aion Tech, Odoo Community Association (OCA)",
    "maintainers": [
        "SirAionTech",
    ],
    "license": "AGPL-3",
    "depends": [
        "product",
    ],
    "data": [
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/res_config_settings_views.xml",
    ],
}
