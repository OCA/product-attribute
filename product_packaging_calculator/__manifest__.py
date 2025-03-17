# Copyright 2020 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)
{
    "name": "Product packaging calculator",
    "summary": "Compute product quantity to pick by packaging",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product"],
    "external_dependencies": {
        "python": [
            "openupgradelib",
        ],
    },
    "pre_init_hook": "pre_init_hook",
}
