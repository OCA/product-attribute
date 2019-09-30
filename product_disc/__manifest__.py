# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Product Disc",
    "summary": "Manage music records as products",
    "version": "12.0.1.0.0",
    "development_status": "Alpha",
    "category": "Sales",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
    ],
    "data": [
        "data/product_attribute.xml",
        "data/product_attribute_value_format.xml",
        "data/product_attribute_value_year.xml",
        "views/product_template.xml",
        "views/product_product.xml",
    ],
}
