# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Product Pricelist Fixed Currency Rate",
    "summary": "Set a fixed currency rate between pricelists",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "maintainers": ["LoisRForgeFlow"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product"],
    "data": [
        "views/pricelist_views.xml",
    ],
}
