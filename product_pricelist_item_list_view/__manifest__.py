# Copyright 2016 Lorenzo Battistini - Agile Business Group
# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Pricelist rules list view",
    "summary": "View and search the list of pricelist items",
    "version": "16.0.1.0.0",
    "category": "Sales Management",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Agile Business Group, ForgeFlow, Odoo Community Association (OCA)",
    "maintainers": ["LoisRForgeFlow"],
    "development_status": "Production/Stable",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
    ],
    "data": [
        "views/pricelist_view.xml",
    ],
}
