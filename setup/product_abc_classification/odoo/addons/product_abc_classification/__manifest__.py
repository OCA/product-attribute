# Copyright 2020 ForgeFlow
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Product ABC Classification",
    "summary": "Includes ABC classification for inventory management",
    "version": "15.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Inventory Management",
    "license": "AGPL-3",
    "maintainers": ["MiquelRForgeFlow"],
    "depends": ["sale_stock"],
    "data": [
        "data/ir_cron.xml",
        "security/ir.model.access.csv",
        "views/abc_classification_view.xml",
        "views/product_view.xml",
    ],
    "installable": True,
}
