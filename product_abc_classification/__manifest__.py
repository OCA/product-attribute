# Copyright 2020 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product ABC Classification",
    "summary": "Includes ABC classification for inventory management",
    "version": "13.0.2.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Inventory Management",
    "license": "AGPL-3",
    "maintainers": ["MiquelRForgeFlow"],
    "depends": ["sale_stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_view.xml",
        "views/abc_classification_view.xml",
        "data/ir_cron.xml",
    ],
    "installable": True,
}
