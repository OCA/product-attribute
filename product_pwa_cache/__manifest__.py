# Copyright 2020 Tecnativa - Alexandre D. Díaz
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Product PWA Cache",
    "summary": "Adds support to cache products",
    "version": "12.0.1.0.0",
    "development_status": "Beta",
    "category": "Website",
    "website": "https://github.com/OCA/web",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["Tardo"],
    "license": "LGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        'web_pwa_cache',
    ],
    "data": [
        "data/data.xml",
    ],
}
