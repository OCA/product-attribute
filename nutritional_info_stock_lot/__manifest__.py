# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Nutritional Info Stock Lot",
    "summary": "Nutritional information for lots.",
    "version": "15.0.1.1.0",
    "development_status": "Production/Stable",
    "category": "Technical Settings",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["CarlosRoca13"],
    "license": "AGPL-3",
    "depends": ["nutritional_info", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "report/report_nutritional_info.xml",
        "views/stock_menu_views.xml",
        "views/stock_production_lot_view.xml",
    ],
    "application": False,
    "installable": True,
}
