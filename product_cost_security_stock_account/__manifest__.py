# Copyright 2026 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product cost security stock account",
    "summary": "Glue module between product_cost_security and stock_account",
    "version": "19.0.1.1.4",
    "development_status": "Beta",
    "category": "Stock",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["CarlosRoca13"],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": ["product_cost_security", "stock_account"],
    "data": ["views/stock_account_views.xml"],
    "assets": {
        "web.assets_backend": [
            "product_cost_security_stock_account/static/src/stock_forecasted/forecasted_header.xml",
        ],
    },
}
