# Copyright 2022 Studio73 - Carlos Reyes <carlos@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Attribute Add Description Orders Invoices",
    "summary": "Add attribute value in sale and invoice lines description",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "account",
        "product",
        "sale_product_configurator",
        "sale_management",
        "web",
    ],
    "author": "Studio73, Odoo Community Association (OCA)",
    "category": "Product Management",
    "maintainers": ["Reyes4711-S73"],
    "website": "https://github.com/OCA/product-attribute",
    "data": ["views/product_attribute_views.xml"],
    "installable": True,
}
