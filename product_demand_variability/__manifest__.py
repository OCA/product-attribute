# Copyright 2020 ForgeFlow S.L.(http://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Demand Variability",
    "summary": "Classifies products depending on its demand variability",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "data": [
        "views/profile_variability_view.xml",
        "views/product_views.xml",
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
    ],
    "depends": ["stock", "sale"],
    "external_dependencies": {"python": ["numpy"]},
    "application": False,
    "installable": True,
}
