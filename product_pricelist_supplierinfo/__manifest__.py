# Copyright 2018 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Supplier info prices in sales pricelists",
    "summary": "Allows to create priceslists based on supplier info",
    "version": "17.0.1.0.0",
    "category": "Sales/Sales",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA), Vauxoo",
    "maintainers": ["luisg123v"],
    "license": "AGPL-3",
    "depends": ["product"],
    "data": [
        "security/res_groups.xml",
        "views/product_pricelist_item_views.xml",
        "views/product_supplierinfo_view.xml",
    ],
    "installable": True,
}
