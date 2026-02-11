# Copyright 2026 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Attribute Line Template",
    "version": "18.0.1.0.0",
    "category": "Product",
    "summary": "Define attribute-line templates and apply them to products",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "license": "AGPL-3",
    "depends": [
        "sale_management",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/product_attribute_template_views.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
    "application": False,
}
