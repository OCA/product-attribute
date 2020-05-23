# Copyright 2020 NextERP Romania SRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Brand prices in sales pricelists",
    "summary": "Allows to create priceslists based on product brand",
    "version": "12.0.1.0.0",
    "category": "Sales",
    "website": "https://github.com/OCA/product-attribute",
    "author": "NextERP Romania,"
              " Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "product_brand",
    ],
    "data": [
        "views/product_pricelist_item_views.xml",
    ],
    "installable": True,
}
