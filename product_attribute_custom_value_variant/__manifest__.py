# Copyright 2025 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Create product variant from custom value",
    "summary": "When a custom value is assigned, create a variant instead.",
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Aion Tech, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Sales/Sales",
    "depends": [
        "product",
        "sale",
    ],
    "data": [
        "views/product_attribute_value_views.xml",
    ],
}
