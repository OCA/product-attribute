# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>)
# Copyright (C) 2020 ForgeFlow S.L. (<http://www.forgeflow.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product Catalog",
    "version": "13.0.1.0.0",
    "author": "Tiny, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Generic Modules/Inventory Control",
    "summary": "Print report of product catalog with product image & list price",
    "depends": ["product"],
    "data": [
        "views/product_report.xml",
        "wizard/product_wizard.xml",
        "report/product_catalog.xml",
    ],
    "installable": True,
}
