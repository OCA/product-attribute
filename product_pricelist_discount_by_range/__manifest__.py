# Copyright 2026 Tecnativa - Andrii Kompaniiets
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product Pricelist Discount by Range",
    "summary": "Allows to create priceslists with discount ranges",
    "version": "15.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_pricelist_item_views.xml",
    ],
    "installable": True,
}
