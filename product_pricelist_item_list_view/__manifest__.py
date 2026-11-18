# Copyright 2016 Lorenzo Battistini - Agile Business Group
# Copyright 2023 ForgeFlow S.L. (https://www.forgeflow.com)
# Copyright 2026 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Pricelist rules list view",
    "summary": "View and search the list of pricelist items",
    "version": "14.0.1.1.0",
    "category": "Sales Management",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Agile Business Group, ForgeFlow, Odoo Community Association (OCA), Numigi",
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
