# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Product Dangerous Good",
    "summary": "Allows to set appropriate danger class and components to products",
    "version": "12.0.1.0.0",
    "development_status": "Alpha",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
        "sale",
    ],
    "data": [
        "data/product_dangerous_type_data.xml",
        "data/product_dangerous_class_data.xml",
        "security/ir.model.access.csv",
        "views/product_template_view.xml",
        "views/product_dangerous.xml",
    ],
}
