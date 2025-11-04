# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Multi Code",
    "summary": "Allow multiple internal references (default_code) per product",
    "version": "17.0.1.1.0",
    "category": "Product Management",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product", "stock"],
    "data": [
        "security/group.xml",
        "security/ir.model.access.csv",
        "views/product_views.xml",
        "views/product_template_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
}
