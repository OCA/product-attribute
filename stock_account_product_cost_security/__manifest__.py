# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Account Product Cost Security",
    "summary": "Product cost security restriction view",
    "version": "15.0.1.0.0",
    "development_status": "Production/Stable",
    "maintainers": ["sergio-teruel"],
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": ["stock_account", "product_cost_security"],
    "data": [
        "data/product_cost_security.xml",
        "views/product_views.xml",
        "wizard/stock_change_standard_price_views.xml",
    ],
}
