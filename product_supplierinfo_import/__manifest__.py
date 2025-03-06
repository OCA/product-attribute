# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Import supplier pricelists",
    "summary": "Import supplier pricelists",
    "version": "16.0.3.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["purchase"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_supplierinfo_import_template_views.xml",
        "wizards/product_supplierinfo_import_views.xml",
    ],
}
