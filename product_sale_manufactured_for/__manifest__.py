# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    "name": "Product Manufactured for Customer",
    "summary": "Allows to indicate in products that they were made "
    "specifically for some customers.",
    "version": "14.0.1.2.0",
    "category": "Sales",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "data": [
        "views/product_product.xml",
        "views/sale_order.xml",
    ],
    "depends": [
        "product",
        "sale",
        "sale_commercial_partner",
    ],
}
