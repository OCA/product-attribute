# Copyright 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Tier Validation",
    "summary": "Support a tier validation process for Products",
    "version": "14.0.2.0.0",
    "website": "https://github.com/OCA/product-attribute",
    "category": "Products",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "maintainers": ["dreispt"],
    "development_status": "Beta",
    "depends": ["product_state", "base_tier_validation"],
    "data": [
        "data/tier_definition.xml",
        "views/product_template_view.xml",
    ],
}
