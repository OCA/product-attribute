# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Secondary Unit",
    "summary": "Set a secondary unit per product",
    "version": "16.0.1.0.2",
    "development_status": "Production/Stable",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product"],
    "data": ["security/ir.model.access.csv", "views/product_views.xml"],
    "maintainers": ["sergio-teruel"],
}
