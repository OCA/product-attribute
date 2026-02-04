# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Import supplier pricelists set margins",
    "summary": "Import supplier pricelists and margins",
    "version": "18.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "product_supplierinfo_import",
        "product_pricelist_supplierinfo",
    ],
    "data": [
        "wizards/product_supplierinfo_import_views.xml",
    ],
}
