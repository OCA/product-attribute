# Copyright 2024 Binhex - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Amount overcharge in sales pricelists",
    "summary": "Allows to add/substract amount to the final priceslists price",
    "version": "14.0.0.1.0",
    "category": "Sales",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Binhex, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_pricelist_item_views.xml",
    ],
    "installable": True,
}
