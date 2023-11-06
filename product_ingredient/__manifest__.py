# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Ingredients",
    "summary": "Product ingredients",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Technical Settings",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["sergio-teruel"],
    "license": "AGPL-3",
    "depends": ["product", "stock"],
    "external_dependencies": {"python": ["openupgradelib"]},
    "data": [
        "security/ir.model.access.csv",
        "data/product_allergen_data.xml",
        "views/product_attribute_value_views.xml",
        "views/product_ingredient_views.xml",
        "views/product_views.xml",
        "views/stock_production_lot_view.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "application": False,
    "installable": True,
}
